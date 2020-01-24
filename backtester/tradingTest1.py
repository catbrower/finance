from datetime import datetime, timedelta
from threading import Lock, Thread
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import csv
import numpy as np
import pandas as pd
import QuandlFetch
import Strategy, Controller, DataProvider

class OderApi:
    def ___init___(self):
        self.slippage_std = .01
        self.prob_of_failure = 0 #.0001
        self.fee = .02
        self.fixed_fee = 10
        self.calculate_fee = lambda x: self.fee * abs(x) + self.fixed_fee

    def process_order(self, order):
        slippage = np.random.normal(0, self.slippage_std, size=1)[0]

        if(np.random.choice([False, True], p=[self.prob_of_failure, 1 - self.prob_of_failure], size=1)[0]):
            trade_fee = self.fee * order[1] * (1 + slippage) * order[2]
            return (order[0], order[1] * (1 + slippage), order[2], self.calculate_fee(trade_fee))

strategy = Strategy.Strategy()
controller = Controller.Controller('2019-01-01', '2020-01-01', strategy)
controller.begin()