#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import core.core_logging as log

logging = log.get_logger()


def api_test(method, url, data):
    try:
        if method == 'get':
            result = requests.get(url, data)
        if method == 'post':
            result = requests.post(url, data)

        response = result.json()
        code = response.get('errorCode')
        info = response.get('errorInfo')
        return code
    except Exception as e:
        logging.error('service error', e)

