import base64
import hashlib
import hmac
import json
import datetime
import urllib
from urllib.parse import urlencode

import requests


class Client_okx():

    API_KEY = "b647e4ab-4f21-4575-b3dd-bfe3f2e238bd"
    API_SECRET = "F6DD8B3107A12A024464F4C39DE2D71E"
    PASSPHRASE = "Ololodota76."

    def get_timestamp(self):
        now = datetime.datetime.utcnow()
        timestamp = now.isoformat("T", "milliseconds")
        return timestamp + "Z"

    def sign(self, timestamp, method, request_path, body):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        prehash = str(timestamp) + str.upper(method) + request_path + str(body)
        print(prehash)
        key = hmac.new(bytes(self.API_SECRET, encoding='utf-8'), bytes(prehash, encoding='utf-8'), digestmod='sha256').digest()
        return base64.b64encode(key)


    def get_headers(self, sign, timestamp):
        header = dict()
        header['Content-Type'] = 'application/json'
        header['OK-ACCESS-KEY'] = self.API_KEY
        header['OK-ACCESS-SIGN'] = sign
        header['OK-ACCESS-TIMESTAMP'] = str(timestamp)
        header['OK-ACCESS-PASSPHRASE'] = self.PASSPHRASE
        header['Accept'] = 'text/plain'
        header['x-simulated-trading'] = '1'

        return header

    def __parse_params_to_str(self, params):
        url = '?'
        for key, value in params.items():
            url = url + str(key) + '=' + urllib.parse.quote(str(value), safe='') + '&'
        return url[0:-1]


    def get_open_orders(self):
            timestamp = okx.get_timestamp()
            url = 'https://www.okx.com/api/v5/trade/orders-pending'
            headers = okx.get_headers((okx.sign(timestamp, "GET", "/api/v5/trade/orders-pending", '')), timestamp)
            self.orders = requests.get(url, headers=headers)
            to_json = json.loads(self.orders.text)['data']
            self.tickers = []
            self.order_id = []
            for i in range(len(to_json)):
                self.tickers.append(to_json[i]['instId'])
                self.order_id.append(to_json[i]['ordId'])
            print(*self.tickers)
            print(*self.order_id)
            okx.post()

    def post(self):
        timestamp = okx.get_timestamp()
        base_url = 'https://www.okx.com'
        request_path = '/api/v5/trade/cancel-order'
        params = {'instId': 'LTC-USDT-220930', 'ordId':'476932512397262848'}
        url = base_url + request_path
        header = okx.get_headers(okx.sign(timestamp, 'POST', request_path, json.dumps(params)), timestamp)
        print(header)
        response = requests.post(url, json=params, headers=header)
        print(response.request.body)
        print(response.text)
        return response.text

okx = Client_okx()
okx.get_open_orders()