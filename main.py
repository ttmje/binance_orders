from urllib.parse import urlencode
import requests
import json
import hmac, hashlib
import time
from pynput.keyboard import Key, Listener

class Client():

    API_KEY = "6d8b6d8be60c37121c60ea2b26134d2a7fd960832464c9db5857c57d47a8f46c"
    API_SECRET = "8555db4d12b17ea2ece76768841f931edf12672806dfe0b87de85e7b9796cfe5"
    timestamp = int(time.time()*1000)
    symbol = 'BTCUSDT'

    def check_con(self):
        ping = requests.get('https://testnet.binancefuture.com/fapi/v1/ping')
        time = requests.get('https://testnet.binancefuture.com/fapi/v1/time')
        if ping.text == "{}":
            print("Success", time.text)

    def get_open_orders(self):
        self.querystring = urlencode({'timestamp': self.timestamp, 'recvWindow': 10000})
        self.key = hmac.new(self.API_SECRET.encode('utf-8'), self.querystring.encode('utf-8'),digestmod=hashlib.sha256).hexdigest()
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'X-MBX-APIKEY': self.API_KEY}
        url = f'https://testnet.binancefuture.com/fapi/v1/openOrders?{self.querystring}&signature={self.key}'
        self.orders = requests.get(url, headers=headers)
        self.count = len(json.loads(self.orders.text))
        self.tickers = []
        for i in range(len(json.loads(self.orders.text))):
            self.tickers.append(json.loads(self.orders.text)[i]['symbol'])
        print('Open orders count:', self.count, 'tickers is:', *self.tickers)



    def close_all_pos(self):
            if self.count != 0:
                user_symbol = input('Type ticker for cancel or press [ENTER] to cancel ALL open orders: ')
                if user_symbol != '':
                    self.symbol = user_symbol
                    self.querystring = urlencode({'symbol': self.symbol, 'timestamp': self.timestamp, 'recvWindow': 10000})
                    self.key = hmac.new(self.API_SECRET.encode('utf-8'), self.querystring.encode('utf-8'),digestmod=hashlib.sha256).hexdigest()
                    headers = {'Content-type': 'application/x-www-form-urlencoded', 'X-MBX-APIKEY': self.API_KEY}
                    url = f'https://testnet.binancefuture.com/fapi/v1/allOpenOrders?{self.querystring}&signature={self.key}'
                    r = requests.delete(url, headers=headers)
                    print(url)
                    print(r.text)
                else:
                    for i in range(len(self.tickers)):
                        self.symbol = self.tickers[i]
                        self.querystring = urlencode({'symbol': self.symbol, 'timestamp': self.timestamp, 'recvWindow': 10000})
                        self.key = hmac.new(self.API_SECRET.encode('utf-8'), self.querystring.encode('utf-8'),digestmod=hashlib.sha256).hexdigest()
                        headers = {'Content-type': 'application/x-www-form-urlencoded', 'X-MBX-APIKEY': self.API_KEY}
                        url = f'https://testnet.binancefuture.com/fapi/v1/allOpenOrders?{self.querystring}&signature={self.key}'
                        r = requests.delete(url, headers=headers)
                        print(url)
                        print(r.text)
            else:
                print('[There is no open orders to cancel]')


if __name__ == '__main__':
    task = Client()
    task.check_con()
    task.get_open_orders()
    task.close_all_pos()
