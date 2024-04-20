import time 
from urllib.parse import urlencode

from .error import ParameterRequiredError

def get_timestamp():
    return int(time.time() * 1000)


def cleanNoneValue(d) -> dict:
    out = {}
    for k in d.keys():
        if d[k] is not None:
            out[k] = d[k]
    return out


def encoded_string(query):
    return urlencode(query, True).replace("%40", "@")


def check_required_parameter(value, name):
    if not value and value != 0:
        raise ParameterRequiredError([name])