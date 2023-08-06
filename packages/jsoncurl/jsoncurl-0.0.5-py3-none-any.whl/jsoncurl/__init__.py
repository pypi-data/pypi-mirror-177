#!/usr/bin/env python
import ast
import sys
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import requests


def eval_value(value):
    try:
        return ast.literal_eval(value)
    except Exception:
        return value


def jsoncurl():
    url = sys.argv[1]
    if not url.startswith('http'):
        url = 'http://' + url

    json = {}
    for arg in sys.argv[2:]:
        key, value = arg.split('=')
        value = eval_value(value)
        json[key] = value

    if not json:
        resp = requests.get(url)
    else:
        msg = {'url': url, 'json_input': json}
        print(msg)
        resp = requests.post(url, json=json)

    try:
        print(resp.json())
    except Exception as e:
        print(e)
        print(resp.text)
