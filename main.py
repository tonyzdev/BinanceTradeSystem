# %%
from quant import quant, exchange, method, trader
import getopt, sys
from configparser import ConfigParser
from loguru import logger
import os

logfile_path = os.path.join("log", "run.log")
logger.add(logfile_path, enqueue=True)

if __name__ == "__main__":

    api_key, secret_key = '', ''
    optlist, args = getopt.getopt(sys.argv[1:], '', ['apikey=', 'secretkey='])
    for o, a in optlist:
        if o == '--apikey':
            api_key = a
        if o == '--secretkey':
            secret_key = a

    assert (api_key != '' or secret_key != '')
    bn = exchange.BinanceCex(api_key, secret_key, timeout=1)

    parse = ConfigParser()
    parse.read("config.ini",encoding="utf-8")

    symbol = parse.get("default","SYMBOL")
    max_usd = parse.get("default","MAXUSD")
    max_ratio = parse.get("default","MAXRATIO")

    symbol_config = {
        "name": symbol,
        "max_usd": float(max_usd),
        "max_ratio": float(max_ratio),
    }
    print(symbol_config)

    bot = quant.Quant1(symbol_config, method.M2(), trader.Trader0(), bn)
    bot.run()
