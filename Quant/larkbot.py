import requests
from .lib.stdjson import StdJson

sj = StdJson()


class LarkBot:
    def __init__(self):
        super().__init__()
        self.url = "https://open.feishu.cn/open-apis/bot/v2/hook/............."

    def send(self, data):
        headers = {
            "Content-Type": "application/json"
        }
        res = requests.post(self.url, json=data, headers=headers)
        print(res.text)

    def info(self, msg):
        if msg['title'] == "open":
            self.send(data=sj.trade_msg(msg))
        if msg['title'] == "close":
            self.send(data=sj.cover_msg(msg))

    def warning(self, msg):
        pass

    def error(self, msg):
        self.send(data=sj.error_msg(msg))


if __name__ == "__main__":
    bot = LarkBot()
    info_test = {
        "title": "close",
        "type": "long",
        "time": "2022-01-01 19:00:00",
        "symbol": "ETHUSDT",
        "price": 1000.00,
        "vol": 1,
        "oi": 1,
        "oi_range": "(1,2)",
        "lr": 1,
        "lr_range": "(1,2)",
        "return": 0
    }
    error_test = {
        "time": "2022-01-01 19:00:00",
        "symbol": "ETHUSDT",
        "level": 2,
        "type": "网络错误",
        "content": "下单失败"
    }
    # bot.error(error_test)
    # bot.info(info_test)
