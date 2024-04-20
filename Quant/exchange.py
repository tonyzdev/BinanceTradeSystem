import hmac
import json
import logging
import hashlib
from json import JSONDecodeError
from datetime import datetime
import requests
from .lib.error import ClientError, ServerError
from .lib.utils import get_timestamp
from .lib.utils import cleanNoneValue
from .lib.utils import encoded_string
from .lib.utils import check_required_parameter


class API(object):
    """API base class

    Keyword Args:
        base_url (str, optional): the API base url, useful to switch to testnet, etc. By default it's https://api.binance.com
        timeout (int, optional): the time waiting for server response, number of seconds. https://docs.python-requests.org/en/master/user/advanced/#timeouts
        proxies (obj, optional): Dictionary mapping protocol to the URL of the proxy. e.g. {'https': 'http://1.2.3.4:8080'}
        show_limit_usage (bool, optional): whether return limit usage(requests and/or orders). By default, it's False
        show_header (bool, optional): whether return the whole response header. By default, it's False
    """

    def __init__(
        self,
        key=None,
        secret=None,
        spot_base_url=None,
        future_base_url=None,
        timeout=None,
        proxies=None,
        show_limit_usage=False,
        show_header=False,
    ):
        self.key = key
        self.secret = secret
        self.timeout = timeout
        self.show_limit_usage = False
        self.show_header = False
        self.proxies = None
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json;charset=utf-8",
                "User-Agent": "vonfund/" + "1.0",
                "X-MBX-APIKEY": key,
            }
        )

        if spot_base_url:
            self.spot_base_url = spot_base_url

        if future_base_url:
            self.future_base_url = future_base_url

        if show_limit_usage is True:
            self.show_limit_usage = True

        if show_header is True:
            self.show_header = True

        if type(proxies) is dict:
            self.proxies = proxies

        self._logger = logging.getLogger(__name__)
        return

    def query(self, base_url, url_path, payload=None):
        return self.send_request("GET", base_url, url_path, payload=payload)

    def limit_request(self, http_method, url_path, payload=None):
        """limit request is for those endpoints require API key in the header"""

        check_required_parameter(self.key, "apiKey")
        return self.send_request(http_method, url_path, payload=payload)

    def sign_request(self, http_method, base_url, url_path, payload=None):
        if payload is None:
            payload = {}
        payload["timestamp"] = get_timestamp()
        query_string = self._prepare_params(payload)
        signature = self._get_sign(query_string)
        payload["signature"] = signature
        return self.send_request(http_method, base_url, url_path, payload)

    def limited_encoded_sign_request(self, http_method, url_path, payload=None):
        """This is used for some endpoints has special symbol in the url.
        In some endpoints these symbols should not encoded
        - @
        - [
        - ]

        so we have to append those parameters in the url
        """
        if payload is None:
            payload = {}
        payload["timestamp"] = get_timestamp()
        query_string = self._prepare_params(payload)
        signature = self._get_sign(query_string)
        url_path = url_path + "?" + query_string + "&signature=" + signature
        return self.send_request(http_method, url_path)

    def send_request(self, http_method, base_url, url_path, payload=None):
        if payload is None:
            payload = {}
        url = base_url + url_path
        self._logger.debug("url: " + url)
        params = cleanNoneValue(
            {
                "url": url,
                "params": self._prepare_params(payload),
                "timeout": self.timeout,
                "proxies": self.proxies,
            }
        )

        response = self._dispatch_request(http_method)(**params)
        self._logger.debug("raw response from server:" + response.text)
        self._handle_exception(response)

        try:
            data = response.json()
        except ValueError:
            data = response.text
        result = {}

        if self.show_limit_usage:
            limit_usage = {}
            for key in response.headers.keys():
                key = key.lower()
                if (
                    key.startswith("x-mbx-used-weight")
                    or key.startswith("x-mbx-order-count")
                    or key.startswith("x-sapi-used")
                ):
                    limit_usage[key] = response.headers[key]
            result["limit_usage"] = limit_usage

        if self.show_header:
            result["header"] = response.headers

        if len(result) != 0:
            result["data"] = data
            return result

        return data

    def _prepare_params(self, params):
        return encoded_string(cleanNoneValue(params))

    def _get_sign(self, data):
        m = hmac.new(self.secret.encode("utf-8"), data.encode("utf-8"), hashlib.sha256)
        return m.hexdigest()

    def _dispatch_request(self, http_method):
        return {
            "GET": self.session.get,
            "DELETE": self.session.delete,
            "PUT": self.session.put,
            "POST": self.session.post,
        }.get(http_method, "GET")

    def _handle_exception(self, response):
        status_code = response.status_code
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)
            except JSONDecodeError:
                raise ClientError(status_code, None, response.text, response.headers)
            raise ClientError(status_code, err["code"], err["msg"], response.headers)
        raise ServerError(status_code, response.text)

class BinanceCex(API):
    def __init__(self, key=None, secret=None, **kwargs):
        if "spot_base_url" not in kwargs:
            kwargs["spot_base_url"] = "https://api.binance.com"
        if "future_base_url" not in kwargs:
            kwargs['future_base_url'] = "https://fapi.binance.com"
        
        super().__init__(key, secret, **kwargs)

    def getNowPrice(self, **kwargs):
        kwargs['limit'] = 10
        depth = self.futureOrderBook(**kwargs)
        price = (float(depth['bids'][0][0]) + float(depth['asks'][0][0])) / 2
        return price

    def account(self, **kwargs):
        url_path = "/api/v3/account"
        return self.sign_request("GET", self.spot_base_url, url_path, {**kwargs})

    def futureOrderBook(self, **kwargs):
        url_path = "/fapi/v1/depth"
        return self.query(self.future_base_url, url_path, {**kwargs})

    def futureOpenInterest(self, **kwargs):
        url_path = "/fapi/v1/openInterest"
        return self.query(self.future_base_url, url_path, {**kwargs})

    def futureOpenInterestHist(self, **kwargs):
        url_path = "/futures/data/openInterestHist"
        return self.query(self.future_base_url, url_path, {**kwargs})

    def futureMarketOrder(self, **kwargs):
        url_path = "/fapi/v1/order"
        kwargs['type'] = 'MARKET'
        return self.sign_request("POST", self.future_base_url, url_path, {**kwargs})
    
    def futureQueryOrder(self,  **kwargs):
        url_path = "/fapi/v1/order"
        return self.sign_request("GET", self.future_base_url, url_path, {**kwargs})

    def futureQueryAllOrders(self,  **kwargs):    
        url_path = "/fapi/v1/allOrders"
        return self.sign_request("GET", self.future_base_url, url_path, {**kwargs})

    def futureAccount(self, **kwargs):
        url_path = "/fapi/v2/account"
        return self.sign_request("GET", self.future_base_url, url_path, {**kwargs})

    def futureLongShortAccountRatio(self, **kwargs):
        url_path = "/futures/data/globalLongShortAccountRatio"
        return self.query(self.future_base_url, url_path, {**kwargs})
    
    def futureMarkPriceKlines(self, **kwargs):
        url_path = "/fapi/v1/markPriceKlines"
        return self.query(self.future_base_url, url_path, {**kwargs})

if __name__ == "__main__":
    bn = BinanceCex()

    #print(bn.account())
    #depth = bn.futureOrderBook(symbol="ATOMUSDT", limit=10)
    #print(bn.futureOpenInterest(symbol="ATOMUSDT"))
    
    #print(bn.futureOpenInterestHist(symbol='ATOMUSDT', period='5m'))
    #symbol = 'ATOMUSDT'

    #orderId = 'HRHrs5NdmXRUZKJKY9zCQY'
    #print(bn.futureQueryOrder(symbol=symbol, origClientOrderId=orderId))
    #print(bn.marketOrder(symbol=symbol, side='BUY', type='MARKET', quantity=2.0))
    #x = bn.futureAccount(symbol='ATOMUSDT')
    #print(x['totalWalletBalance'])
    #print(x)
    #print(x['totalUnrealizedProfit'])
    #for p in x['positions']:
    #    if p['symbol'] == symbol:
    #        print(p)

