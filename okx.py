import base64
import hashlib
import hmac
import json
import datetime

import requests


class Client_okx():

    API_KEY = "b647e4ab-4f21-4575-b3dd-bfe3f2e238bd"
    API_SECRET = "F6DD8B3107A12A024464F4C39DE2D71E"
    PASSPHRASE = "Ololodota76."

    def get_timestamp(self):
        now = datetime.datetime.utcnow()
        timestamp = now.isoformat("T", "milliseconds")
        return timestamp + "Z"

    def get_open_orders(self):
            time = okx.get_timestamp()
            print(time)
            self.prehash = time + "GET" + "/api/v5/trade/orders-pending" + ''
            self.key = hmac.new(self.API_SECRET.encode('utf-8'), self.prehash.encode('utf-8'), digestmod=hashlib.sha256).digest()
            self.encoded = base64.b64encode(self.key)
            self.headers = {'Content-Type':'application/json',
                            'OK-ACCESS-KEY':self.API_KEY,
                            'OK-ACCESS-SIGN':self.encoded,
                            'OK-ACCESS-TIMESTAMP':time,
                            'OK-ACCESS-PASSPHRASE':self.PASSPHRASE,
                            'x-simulated-trading': '1'}
            url = 'https://www.okx.com/api/v5/trade/orders-pending'
            self.orders = requests.get(url, headers=self.headers)
            print(self.orders.text)



if __name__ == '__main__':
    okx = Client_okx()
    okx.get_open_orders()