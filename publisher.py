# filename: wk11e_publisher.py
# by Narendra for COMP216 (Aug 2020)
# publishes a series of json objects
# We will use json.dumps() to convert to a string
import time
import paho.mqtt.client as mqtt
import json
import numpy as np

import data_generator
from data_generator import Generator


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
        self.generator = Generator(trend, volatility)
        self.client = mqtt.Client()

    def publish(self):
        self.client.publish('STOCKS/' + self.stock_data['Stock Name'], json.dumps(self.stock_data))

    def start_client(self):
        self.client.connect('localhost', 1883)
        self.client.loop_start()
        self.publish()
        while True:
            time.sleep(2)
            self.stock_data['Time'] = time.asctime()
            self.stock_data['Stock Price'] = self.generator.generate_stock_price(self.last_price)
            self.publish()
            print(self.stock_data['Stock Price'])


pub = Publisher(10, 5, 1, 'Tesla')

pub.start_client()
