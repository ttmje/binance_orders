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

    def sign(self, timestamp, method, endpoint, body=''):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        prehash = timestamp + method + endpoint + str(body)
        key = hmac.new(self.API_SECRET.encode('utf-8'), prehash.encode('utf-8'), digestmod=hashlib.sha256).digest()
        encoded = base64.b64encode(key)
        return encoded

    def get_headers(self, sign, timestamp):
        headers = {'Content-Type': 'application/json',
                        'OK-ACCESS-KEY': self.API_KEY,
                        'OK-ACCESS-SIGN': sign,
                        'OK-ACCESS-TIMESTAMP': timestamp,
                        'OK-ACCESS-PASSPHRASE': self.PASSPHRASE,
                        'x-simulated-trading': '1',
                        }
        return headers

    def get_open_orders(self):
            timestamp = okx.get_timestamp()
            url = 'https://www.okx.com/api/v5/trade/orders-pending'
            headers = okx.get_headers((okx.sign(timestamp, "GET", "/api/v5/trade/orders-pending", '')), timestamp)
            self.orders = requests.get(url, headers=headers)
            to_json = json.loads(self.orders.text)['data']
            self.tickers = []
            for i in range(len(to_json)):
                self.tickers.append(to_json[i]['instId'])
            print(*self.tickers)
            okx.close_pos()

    def close_pos(self):
            for i in range(len(self.tickers)):
                timestamp = okx.get_timestamp()
                self.symbol = self.tickers[i]
                params = urlencode({'instId': self.symbol})
                base_url = 'https://www.okx.com'
                request_path = f'/api/v5/trade/cancel-batch-orders?{params}'
                url = base_url + request_path
                headers = okx.get_headers((okx.sign(timestamp, 'POST', request_path, params)), timestamp)
                canceled = requests.post(url, data=params, headers=headers)
                print(canceled.request.url)
                print(canceled.request.body)
                print(canceled.request.headers)
                print(canceled.text)


if __name__ == '__main__':
    okx = Client_okx()
    okx.get_open_orders()