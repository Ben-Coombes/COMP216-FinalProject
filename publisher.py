# filename: wk11e_publisher.py
# by Narendra for COMP216 (Aug 2020)
# publishes a series of json objects
# We will use json.dumps() to convert to a string
import time
import paho.mqtt.client as mqtt
import json
import random
from data_generator import Generator


class Publisher:
    def __init__(self, start_price, volatility, trend, stock_name):
        self.stock_data = {
            'Time': time.asctime(),
            'Stock Price': start_price,
            'Stock Name': stock_name
        }
        self.volatility = volatility
        self.trend = trend
        self.generator = Generator(trend, volatility)
        self.client = mqtt.Client()

    def send_data(self):
        self.stock_data['Time'] = time.asctime()
        self.client.connect('localhost', 1883)
        self.client.publish('STOCKS/' + self.stock_data['Stock Name'], json.dumps(self.stock_data))
        self.client.disconnect()

    def start(self):
        while True:
            current_price = self.stock_data['Stock Price']
            self.stock_data['Stock Price'] = self.generator.generate_stock_price(current_price)
            time.sleep(0.2)
            if random.randint(0, 100) == 1:
                print('failed')
                continue
            if random.randint(0, 200) == 1:
                self.stock_data['Stock Price'] = '######'
            self.send_data()


pub = Publisher(10, 5, 1, 'Tesla')

pub.start()
