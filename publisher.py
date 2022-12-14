# filename: wk11e_publisher.py
# by Narendra for COMP216 (Aug 2020)
# publishes a series of json objects
# We will use json.dumps() to convert to a string
import time
import paho.mqtt.client as mqtt
import json
import random
from data_generator import Generator
from tkinter import *
import threading


class Publisher(threading.Thread):
    def __init__(self, start_price, volatility, trend, stock_name):
        threading.Thread.__init__(self)
        self.daemon = True
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

    def run(self):
        while True:
            if self.isfloat(self.stock_data['Stock Price']):
                current_price = self.stock_data['Stock Price']
            self.stock_data['Stock Price'] = self.generator.generate_stock_price(current_price)
            time.sleep(0.5)
            if random.randint(0, 100) == 1:
                print('failed')
                continue
            if random.randint(0, 20) == 1:
                self.stock_data['Stock Price'] = '######'
            self.send_data()
            print(self.stock_data['Stock Price'])

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False


def create_pub():
    pub = Publisher(200, 5, 0, 'TSLA')
    pub.start()
    print('test')


if __name__ == '__main__':
    master = Tk()
    master.geometry("700x700")

    create_button = Button(master=master, command=create_pub, height=2, width=10, text="Create")
    create_button.pack()
    master.mainloop()
