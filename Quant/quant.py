# import numpy as np
import time
from datetime import datetime
from loguru import logger
from .larkbot import LarkBot

bot = LarkBot()


class Quant0:
    def __init__(self, symbol_config, method, trader, exchange):
        self.symbol = symbol_config['name']
        self.max_usd = symbol_config['max_usd']
        self.max_ratio = symbol_config['max_ratio']
        self.max_try = 5
        self.method = method
        self.trader = trader
        self.exchange = exchange

    def get_account_info(self):
        pass

    def exec_load_factor(self):
        for _ in range(self.max_try):
            try:
                data = self.method.load_factor(self.exchange, self.symbol)
                if data:
                    return data
            except Exception as ex:
                print(ex)
                time.sleep(1)
        return False

    def exec_method(self, factor_data):
        for _ in range(self.max_try):
            # try:
            trade_data = self.method.run(factor_data)
            if trade_data:
                return trade_data
        # except Exception as ex:
        #    print(ex)
        #    time.sleep(1)
        return False

    def exec_trade(self, trade_data):
        for _ in range(self.max_try):
            try:
                result = self.trader.safe_run(self.exchange, trade_data, self.symbol, self.max_usd, self.max_ratio)
                if result:
                    return result
            except Exception as ex:
                print(ex)
                time.sleep(1)
        return False

    def run(self):
        lastTime = 0
        while True:
            if time.time() - lastTime > 60 * 4.5:
                factor_data = self.exec_load_factor()
                if factor_data:
                    trade_data = self.exec_method(factor_data)
                    if trade_data:
                        if self.exec_trade(trade_data):
                            print("trade_type:\t\t|{}|".format(trade_data['type']))
                        else:
                            bot.error(
                                {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                                 "symbol": self.symbol,
                                 "level": 3,
                                 "type": "下单错误",
                                 "content": "下单执行错误"})
                            time.sleep(10)
                    else:
                        bot.error(
                            {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                             "symbol": self.symbol,
                             "level": 2,
                             "type": "计算错误",
                             "content": "指标计算错误"})
                        time.sleep(10)
                else:
                    # print("Error!\t|\tCan not load factor data.")
                    bot.error(
                        {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                         "symbol": self.symbol,
                         "level": 3,
                         "type": "网络错误",
                         "content": "数据读取错误"})
                    time.sleep(10)

                lastTime = time.time()
            else:
                print("{}\t|\t{}".format(time.asctime(time.localtime(time.time())), "health running."))
                time.sleep(10)


class Quant1:
    def __init__(self, symbol_config, method, trader, exchange):
        self.symbol = symbol_config['name']
        self.max_usd = symbol_config['max_usd']
        self.max_ratio = symbol_config['max_ratio']
        self.max_try = 10
        self.method = method
        self.trader = trader
        self.exchange = exchange
        self.record = [1]

    def get_account_info(self):
        pass

    def exec_load_factor(self):
        beginTime = time.time() // 300 * 300
        while True:
            trade_data = self.method.load_factor(self.exchange, self.symbol)
            if trade_data:
                return trade_data
            time.sleep(2)
            # logger.info("wait for data")
            if time.time() // 300 * 300 - beginTime >= 300:
                # 如果超过5分钟请求不到数据, 自动退出
                return 0

    def exec_method(self, factor_data):
        for _ in range(self.max_try):
            try:
                data = self.method.run(factor_data)
                if data:
                    return data
            except Exception as ex:
                logger.debug(ex)
                time.sleep(1)
        return False

    def exec_trade(self, trade_data):
        for _ in range(self.max_try):
            try:
                result = self.trader.safe_run(self.exchange, trade_data, self.symbol, self.max_usd, self.max_ratio)
                if result:
                    return result
            except Exception as ex:
                logger.debug(ex)
                time.sleep(1)
        return False

    def run(self):

        while True:
            begin = time.time() // 300 * 300
            logger.info("health running")
            # Todo:
            # 完善各返回状态码,之后根据状态码进行log返回
            factor_data = self.exec_load_factor()
            if factor_data:
                trade_data = self.exec_method(factor_data)
                if trade_data:
                    if self.exec_trade(trade_data):
                        logger.info("trade_type: |{}|".format(trade_data['type']))
                        time.sleep(begin + 300 - time.time())
                    else:
                        logger.debug("cannot trade")
                        bot.error(
                            {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                             "symbol": self.symbol,
                             "level": 3,
                             "type": "下单错误",
                             "content": "下单执行错误"})
                        time.sleep(begin + 300 - time.time())

                else:
                    logger.debug("cannot run method")
                    bot.error(
                        {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                         "symbol": self.symbol,
                         "level": 2,
                         "type": "计算错误",
                         "content": "指标计算错误"})
                    time.sleep(begin + 300 - time.time())

            else:
                logger.debug("cannot load factor data")
                bot.error({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                           "symbol": self.symbol,
                           "level": 3,
                           "type": "网络错误",
                           "content": "数据读取错误"})
                time.sleep(begin + 300 - time.time())
