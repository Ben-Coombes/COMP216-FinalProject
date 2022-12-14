# filename: wk11e_publisher.py
# by Narendra for COMP216 (Aug 2020)
# publishes a series of json objects
# We will use json.dumps() to convert to a string
import time
import paho.mqtt.client as mqtt
import json
import numpy as np


class Publisher:
    def __init__(self, start_price, volatility, trend, stock_name):
        self.stock_data = {
            'Time': time.asctime(),
            'Stock Price': start_price,
            'Stock Name': stock_name
        }
        self.last_price = start_price
        self.volatility = volatility
        self.trend = trend

    def start_client(self):
        client = mqtt.Client()
        client.connect('localhost', 1883)
        client.loop_start()
        client.publish('STOCKS/' + self.stock_data['Stock Name'], json.dumps(self.stock_data))
        time.sleep(1)
        while True:
            time.sleep(15)
            self.stock_data['Time'] = time.asctime()
            self.stock_data['Stock Price'] = self.generate_stock_price()
            client.publish('STOCKS/' + self.stock_data['Stock Name'], json.dumps(self.stock_data))
            print(self.stock_data['Stock Price'])

    def generate_stock_price(self):
        price = self.last_price + self.trend + (1 + np.random.normal(0, self.volatility))
        self.last_price = price
        return price


pub = Publisher(10, 5, 1, 'Tesla')

pub.start_client()
