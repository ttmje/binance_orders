from urllib.parse import urlencode
import requests
import websockets
import json
import hmac, hashlib
import time

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

    def hmac_gen(self):
       self.querystring = urlencode({'symbol' : self.symbol, 'timestamp' : self.timestamp})
       self.key = hmac.new(self.API_SECRET.encode('utf-8'), self.querystring.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

    def close_all_pos(self):
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'X-MBX-APIKEY': self.API_KEY}
        url = f'https://testnet.binancefuture.com/fapi/v1/allOpenOrders?{self.querystring}&signature={self.key}'
        r = requests.delete(url, headers=headers)
        print(r.text)


if __name__ == '__main__':
    task = Client()
    task.hmac_gen()
    task.check_con()
    task.close_all_pos()