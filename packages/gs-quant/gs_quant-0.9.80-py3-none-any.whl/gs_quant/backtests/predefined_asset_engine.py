"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

from gs_quant.backtests.event import *
from gs_quant.backtests.action_handler import ActionHandlerBaseFactory, ActionHandler
from gs_quant.backtests.actions import Action, AddTradeAction, AddTradeActionInfo
from gs_quant.backtests.backtest_engine import BacktestBaseEngine
from gs_quant.backtests.backtest_objects import PredefinedAssetBacktest
from gs_quant.backtests.execution_engine import SimulatedExecutionEngine
from gs_quant.backtests.core import ValuationMethod
from gs_quant.backtests.data_sources import DataManager
from gs_quant.backtests.order import *
from gs_quant.datetime import is_business_day, prev_business_date, business_day_offset
from pandas import bdate_range, to_datetime
from pandas.tseries.offsets import BDay
from collections import deque
from pytz import timezone
from functools import reduce
import datetime as dt
from typing import Union, Tuple
from tqdm import tqdm

# Action Implementations


class AddTradeActionImpl(ActionHandler):
    def __init__(self, action: AddTradeAction):
        super().__init__(action)

    def generate_orders(self, state: dt.datetime, backtest: PredefinedAssetBacktest, info: AddTradeActionInfo):

        orders = []
        for pricable in self.action.priceables:
            quantity = pricable.instrument_quantity * 1 if info is None else info.scaling
            orders.append(OrderAtMarket(instrument=pricable,
                                        quantity=quantity,
                                        generation_time=state,
                                        execution_datetime=state,
                                        source=self.action._name))
            if isinstance(self.action.trade_duration, dt.timedelta):
                # create close order
                orders.append(OrderAtMarket(instrument=pricable,
                                            quantity=quantity * -1,
                                            generation_time=state,
                                            execution_datetime=state + self.action.trade_duration,
                                            source=self.action._name))
        return orders

    def apply_action(self, state: dt.datetime, backtest: PredefinedAssetBacktest, info=None):
        orders = self.generate_orders(state, backtest, info)
        return orders


class SubmitOrderActionImpl(ActionHandler):
    """
    The apply_action method simply returns the orders generated by the trigger.
    """
    def __init__(self, action: Action):
        super().__init__(action)

    def apply_action(self, state: dt.datetime, backtest: PredefinedAssetBacktest, info=None):
        return info


class PredefinedAssetEngineActionFactory(ActionHandlerBaseFactory):
    def __init__(self, action_impl_map=None):
        action_impl_map = action_impl_map or {}
        self.action_impl_map = action_impl_map
        self.action_impl_map[AddTradeAction] = AddTradeActionImpl

    def get_action_handler(self, action: Action) -> Action:
        if type(action) in self.action_impl_map:
            return self.action_impl_map[type(action)](action)
        raise RuntimeError(f'Action {type(action)} not supported by engine')


class PredefinedAssetEngine(BacktestBaseEngine):

    def get_action_handler(self, action: Action) -> Action:
        handler_factory = PredefinedAssetEngineActionFactory(self.action_impl_map)
        return handler_factory.get_action_handler(action)

    def supports_strategy(self, strategy):
        all_actions = reduce(lambda x, y: x + y, (map(lambda x: x.actions, strategy.triggers)))
        try:
            for x in all_actions:
                self.get_action_handler(x)
        except RuntimeError:
            return False
        return True

    def __init__(self,
                 data_mgr: DataManager = DataManager(),
                 calendars: Union[str, Tuple[str, ...]] = 'Weekend',
                 tz: timezone = timezone('UTC'),
                 valuation_method: ValuationMethod = ValuationMethod(ValuationFixingType.PRICE),
                 action_impl_map=None):
        if action_impl_map is None:
            action_impl_map = {Action: SubmitOrderActionImpl}
        self.action_impl_map = action_impl_map
        self.calendars = calendars
        self.tz = tz
        self.data_handler = DataHandler(data_mgr, tz=tz)
        self.valuation_method = valuation_method
        self.execution_engine = None

    def _eod_valuation_time(self):
        if self.valuation_method.window:
            return self.valuation_method.window.end
        else:
            return dt.time(23)

    def _timer(self, strategy, start, end, frequency, states=None):
        dates = list(map(lambda x: x.date(), to_datetime(bdate_range(start=start, end=end, freq=frequency)))) \
            if states is None else states

        all_times = []
        times = list()
        for trigger in strategy.triggers:
            if hasattr(trigger, 'get_trigger_times'):
                for t in trigger.get_trigger_times():
                    # allow user to define their trigger times as a time, in which case add that time to every date
                    # or as a datetime itself in which case just add it to the timer
                    if isinstance(t, dt.datetime):
                        all_times.append(t)
                    else:
                        times.append(t)
        times.append(self._eod_valuation_time())
        times = list(dict.fromkeys(times))

        for d in dates:
            if isinstance(d, dt.datetime):
                if self.calendars == 'Weekend' or is_business_day(d.date(), self.calendars):
                    all_times.append(d)
                    for t in times:
                        if d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None:
                            all_times.append(d.tzinfo.localize(dt.datetime.combine(d.date(), t)))
            else:
                if self.calendars == 'Weekend' or is_business_day(d, self.calendars):
                    for t in times:
                        all_times.append(dt.datetime.combine(d, t))
        all_times = list(set(all_times))
        all_times.sort()
        return all_times

    def _adjust_date(self, date):
        date = (date + BDay(1) - BDay(1)).date()  # 1st move to latest weekday.
        if self.calendars == 'Weekend' or is_business_day(date, self.calendars):
            return date
        else:
            return prev_business_date(date, self.calendars)

    def run_backtest(self, strategy, start, end, frequency="B", states=None, initial_value=100):
        # initialize backtest object
        self.data_handler.reset_clock()
        backtest = PredefinedAssetBacktest(self.data_handler, initial_value)

        # initialize execution engine
        self.execution_engine = SimulatedExecutionEngine(self.data_handler)

        if states is not None:
            timer = self._timer(strategy, start, end, frequency, states)
        else:
            # if start is a holiday, go back to the previous day on the backtest calendar
            adjusted_start = self._adjust_date(start)
            backtest.set_start_date(adjusted_start)

            # create timer
            timer_start = (adjusted_start + BDay(1)).date() if self.calendars == 'Weekend' \
                else business_day_offset(adjusted_start, 1, roll='forward', calendars=self.calendars)
            timer_end = self._adjust_date(end)
            timer = self._timer(strategy, timer_start, timer_end, frequency)
        self._run(strategy, timer, backtest)
        return backtest

    def _run(self, strategy, timer, backtest: PredefinedAssetBacktest):
        events = deque()

        for state in tqdm(timer):
            # update to latest data
            self.data_handler.update(state)

            # see if any submitted orders have been executed
            fills = self.execution_engine.ping(state)
            events.extend(fills)

            # generate a market event
            events.append(MarketEvent())

            # create valuation event when it's due for daily valuation
            if state.time() == self._eod_valuation_time():
                events.append(ValuationEvent())

            while events:
                event = events.popleft()

                if event.type == 'Market':  # market event (new mkt data coming in)
                    for trigger in strategy.triggers:
                        trigger_info = trigger.has_triggered(state, backtest)
                        if trigger_info.triggered:
                            for action in trigger.actions:
                                info_dict = trigger_info.info_dict
                                info = info_dict[type(action)] if info_dict and type(action) in info_dict else None
                                orders = self.get_action_handler(action).apply_action(state, backtest, info)
                                backtest.record_orders(orders)
                                events.extend([OrderEvent(o) for o in orders])
                elif event.type == 'Order':  # order event (submit the order to execution engine)
                    self.execution_engine.submit_order(event)
                elif event.type == 'Fill':  # fill event (update backtest with the fill results)
                    backtest.update_fill(event)
                elif event.type == 'Valuation':  # valuation event (calculate daily level)
                    backtest.mark_to_market(state, self.valuation_method)

        return backtest
