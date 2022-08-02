from urllib.parse import urlparse, parse_qs
from urllib.parse import urlencode
import requests
import json
import hmac, hashlib
import time
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'segwergergwergwergwergwer5gy34525345'
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form.get('get_open_orders'):
           if task.get_open_orders() == []:
              flash(f"Open orders: 0")
           else:
              flash(f"Open orders: {task.get_open_orders()}")
           return render_template("index.html")

        elif request.form.get('close_all_orders'):
            flash(f'Closed: {task.close_pos()} Open: {task.get_orders_count()}')
            return render_template("index.html")

        elif request.form.get('close_one'):
            try:
                user_symbol = request.form.get('ticker')
                if len(user_symbol) <= 7:
                    flash(f'Closed: {task.close_one(user_symbol)} Open: {task.get_orders_count()}')
                    return render_template("index.html")
                else:
                    return render_template("index.html")
            except:
                return render_template("index.html")
    else:
        return render_template("index.html")

class Client():
    API_KEY = "6d8b6d8be60c37121c60ea2b26134d2a7fd960832464c9db5857c57d47a8f46c"
    API_SECRET = "8555db4d12b17ea2ece76768841f931edf12672806dfe0b87de85e7b9796cfe5"
    symbol = 'BTCUSDT'

    def check_con(self):
        ping = requests.get('https://testnet.binancefuture.com/fapi/v1/ping')
        time = requests.get('https://testnet.binancefuture.com/fapi/v1/time')
        if ping.text == "{}":
            print("Success", time.text)

    def get_open_orders(self):
        self.timestamp = int(time.time() * 1000)
        self.querystring = urlencode({'timestamp': self.timestamp, 'recvWindow': 15000})
        self.key = hmac.new(self.API_SECRET.encode('utf-8'), self.querystring.encode('utf-8'),digestmod=hashlib.sha256).hexdigest()
        self.headers = {'Content-type': 'application/x-www-form-urlencoded', 'X-MBX-APIKEY': self.API_KEY}
        url = f'https://testnet.binancefuture.com/fapi/v1/openOrders?{self.querystring}&signature={self.key}'
        self.orders = requests.get(url, headers=self.headers)
        self.count = len(json.loads(self.orders.text))
        self.tickers = []
        for i in range(len(json.loads(self.orders.text))):
            self.tickers.append(json.loads(self.orders.text)[i]['symbol'])
        print('Open orders count:', self.count, ', tickers is:', *self.tickers)
        return self.tickers


    def close_pos(self):
        try:
            for i in range(len(self.tickers)):
                self.symbol = self.tickers[i]
                task.urlgen()
                self.symbol = []
            if json.loads(self.r.text)['code'] == 200:
                print('Closed:', len(self.tickers), 'Open:', task.get_orders_count())
                b = self.tickers
            else:
                errors = urlparse(self.url)
                err = (parse_qs(errors[4]))
                tkr = err["symbol"]
                itemstoremove = set(err["symbol"])
                b = [x for x in self.tickers if x not in itemstoremove]
                print(f'Error! {len(tkr)}, Closed: {len(b)}, Open:, {task.get_orders_count()}')
        except:
            print('Orders not found, get open orders')
        return len(b)

    def close_one(self, user_symbol):
        try:
            if self.count != 0:
                user_symbol = request.form.get('ticker')
                if user_symbol != '':
                    self.symbol = user_symbol
                    task.urlgen()
                    self.tickers.remove(user_symbol.upper())
                else:
                    print('There is no orders to cancel')
        except:
            print('Error')
            return "error, wrong ticker"
        return user_symbol


    def get_orders_count(self):
        self.timestamp = int(time.time() * 1000)
        self.querystring = urlencode({'timestamp': self.timestamp, 'recvWindow': 15000})
        self.key = hmac.new(self.API_SECRET.encode('utf-8'), self.querystring.encode('utf-8'),
                            digestmod=hashlib.sha256).hexdigest()
        self.headers = {'Content-type': 'application/x-www-form-urlencoded', 'X-MBX-APIKEY': self.API_KEY}
        url = f'https://testnet.binancefuture.com/fapi/v1/openOrders?{self.querystring}&signature={self.key}'
        self.orders = requests.get(url, headers=self.headers)
        self.count = len(json.loads(self.orders.text))
        return self.count


    def urlgen(self):
        self.timestamp = int(time.time() * 1000)
        self.querystring = urlencode({'symbol': self.symbol, 'timestamp': self.timestamp, 'recvWindow': 10000})
        self.key = hmac.new(self.API_SECRET.encode('utf-8'), self.querystring.encode('utf-8'),digestmod=hashlib.sha256).hexdigest()
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'X-MBX-APIKEY': self.API_KEY}
        self.url = f'https://testnet.binancefuture.com/fapi/v1/allOpenOrders?{self.querystring}&signature={self.key}'
        self.r = requests.delete(self.url, headers=headers)
        self.symbol = []
        #print(self.url)
        #print(self.r.text)

    def save_log(self):
        with open('log.txt', 'a') as f:
            if self.r.status_code == 200:
                f.writelines(f'timestamp: {self.timestamp} url: {self.url}\n message: {self.r.text}\n\n')
            else: f.writelines(f'timestamp: {self.timestamp}, ERROR {self.r.text}')

    def menu(self):
        cmd = input(f'Menu: \n'
                    f'[1] - Check connection\n'
                    f'[2] - Get open orders\n'
                    f'[3] - CLose open orders\n'
                    f'Type command: ')
        while True:
            if cmd == '1':
                task.check_con()
            elif cmd == '2':
                task.get_open_orders()
            elif cmd == '3':
                task.close_pos()
            else:
                print('Wrong command!')
            cmd = input('Type command: ')
        return

if __name__ == '__main__':
    task = Client()
    app.run(debug=False)
    task.menu()



