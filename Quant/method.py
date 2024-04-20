from datetime import datetime
import numpy as np
import gc
import time
from queue import Queue
from collections import deque
from loguru import logger

MA_PERIOD = 13


def backtest():
    #todo
    return


class M0:
    def __init__(self, config={}):
        self.config = config
        self.Period = 12 * self.hours
        self.lastUpdateTime = 0
        self.updateInterval = 60 * 60 * self.hours
        self.dir = "STOP"

    def load_factor(self, exchange, symbol):
        #todo
        return data

    def find_param(self, factor_data):
        return best_param, best_param, best_score

    def update_param(self, factor_data):

        if time.time() - self.lastUpdateTime > self.updateInterval:
            startTime = time.time()
            self.R_iv, self.R_l, best_score = self.find_param(factor_data=factor_data)
            self.lastUpdateTime = time.time()
            print("-----------------------------------------------------------------")
            print("Params update:\tIV:\t{:.2f}\tL:\t{:.2f}\tscore:{}\tTime:\t{}".format(self.R_iv, self.R_l, best_score,
                                                                                        self.lastUpdateTime - startTime))
            print("-----------------------------------------------------------------")

    def run(self, factor_data):

        self.update_param(factor_data=factor_data)
        #todo

        return {"type": self.dir}
