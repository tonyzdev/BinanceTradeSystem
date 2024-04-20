import numpy as np
import time
from loguru import logger
from .larkbot import LarkBot
eps = 1e-6

def find_symbol_position(position, symbol):
    for p in position:
        if p['symbol'] == symbol:
            return p

class Trader0:
    detail = "simple market buy and sell"
    def __init__(self, config = {}):
        self.position = None
        self.max_dec = 3
        self.bot = LarkBot()
        self.last_price = 0

    def safe_run(self, exchange, trade_data, symbol, max_usd, max_ratio):
        return self.run(exchange, trade_data, symbol, max_usd, max_ratio)


    def updatePosition(self, exchange, symbol):
        account = exchange.futureAccount()
        self.position = find_symbol_position(account['positions'], symbol)


    def run(self, exchange, trade_data, symbol, max_usd, max_ratio):
        self.updatePosition(exchange, symbol)

        qty = float(self.position['positionAmt'])
        entryPrice = float(self.position['entryPrice'])
        orderId = 0

        if trade_data['type'] == 'BUY' and np.abs(qty) < eps:
            # Long 
            nowPrice = exchange.getNowPrice(symbol=symbol)
            dec = 10 ** self.max_dec
            needQty = np.floor(max_usd * max_ratio / nowPrice * dec) / dec
            logger.info("long {} {}".format(needQty, dec))
            # self.bot.info("start long {} {} at price {}".format(needQty, symbol, nowPrice))
            resp = exchange.futureMarketOrder(symbol=symbol, side='BUY', quantity=needQty)
            orderId = resp['orderId']
            self.last_price = nowPrice
            self.bot.info(
                {
                    "title":"open",
                    "type":"long",
                    "time":time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()),
                    "symbol":symbol,
                    "price":nowPrice,
                    "vol":needQty,
                    "return":0,
                    "oi":trade_data["oi"],
                    "lr":trade_data["lr"],
                    # "iv_range":trade_data["oi_range"],
                    # "lr_range":trade_data["lr_range"],
                }
            )
            # resp do someting
        
        if trade_data['type'] == 'SELL' and np.abs(qty) < eps:
            # Short 
            nowPrice = exchange.getNowPrice(symbol=symbol)
            dec = 10 ** self.max_dec
            needQty = np.floor(max_usd * max_ratio / nowPrice * dec) / dec
            
            logger.info("short {} {}".format(needQty, dec))
            #self.bot.info("start short {} {} at price {}".format(needQty, symbol, nowPrice))

            resp = exchange.futureMarketOrder(symbol=symbol, side='SELL', quantity=needQty)
            orderId = resp['orderId']
            self.last_price = nowPrice
            self.bot.info(
                {
                    "title":"open",
                    "type": "short",
                    "time":time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()),
                    "symbol":symbol,
                    "price":nowPrice,
                    "vol":needQty,
                    "return":0,
                    "oi":trade_data["oi"],
                    "lr":trade_data["lr"],
                    # "iv_range":trade_data["oi_range"],
                    # "lr_range":trade_data["lr_range"],
                }
            )

        if trade_data['type'] in ['STOP', 'BUY'] and qty < -eps:
            # STOP SHORT
            nowPrice = exchange.getNowPrice(symbol=symbol)
            needQty = np.abs(qty)
            resp = exchange.futureMarketOrder(symbol=symbol, side='BUY', quantity=needQty)
            orderId = resp['orderId']

            logger.info("stop short {}".format(needQty))
            profit = ((self.last_price - nowPrice) / self.last_price - 0.04/100 * 2) #* needQty
            # self.bot.info("stop short {} {} at price {}, profit {}%".format(needQty, symbol, nowPrice, profit))
            self.bot.info(
                {
                    "title":"close",
                    "type":"short",
                    "time":time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()),
                    "symbol":symbol,
                    "price":nowPrice,
                    "vol":needQty,
                    "return":profit,
                    "oi":trade_data["oi"],
                    "lr":trade_data["lr"],
                    # "iv_range":trade_data["oi_range"],
                    # "lr_range":trade_data["lr_range"],
                }
            )


        if trade_data['type'] in ['STOP', 'SELL'] and qty > eps:
            # STOP LONG
            nowPrice = exchange.getNowPrice(symbol=symbol)
            needQty = np.abs(qty)
            resp = exchange.futureMarketOrder(symbol=symbol, side='SELL', quantity=needQty)
            orderId = resp['orderId']
            logger.info("stop long {}".format(symbol, needQty))
            profit = ((nowPrice - self.last_price) / self.last_price - 0.04/100 * 2) 
            # profit = ((self.last_price - nowPrice) / self.last_price - 0.04 * 2)
            # self.bot.info("stop long {} {} at price {}, profit {}%".format(needQty, symbol, nowPrice, profit))
            self.bot.info(
                {
                    "title":"close",
                    "type":"long",
                    "time":time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()),
                    "symbol":symbol,
                    "price":nowPrice,
                    "vol":needQty,
                    "return":profit,
                    "oi":trade_data["oi"],
                    "lr":trade_data["lr"],
                    # "iv_range":trade_data["oi_range"],
                    # "lr_range":trade_data["lr_range"],
                }
            )


        if orderId > 0:
            logger.info("trading got orderId {}".format(orderId))
            for _ in range(10):
                orderInfo = exchange.futureQueryOrder(symbol=symbol, orderId = orderId)
                if orderInfo['status'] == 'FILLED':
                    self.updatePosition(exchange, symbol)
                    return True
                time.sleep(0.5)
            return False
        else:
            return True


            
