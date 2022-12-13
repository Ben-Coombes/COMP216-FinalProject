# filename: wk11e_publisher.py
# by Narendra for COMP216 (Aug 2020)
# publishes a series of json objects
# We will use json.dumps() to convert to a string
import time
import paho.mqtt.client as mqtt
import json


class Publisher:
    my_data = {
        'Time': time.asctime(),
        'x': 0,
        'Stock Price': 10,
    }

    def start_client(self):
        client = mqtt.Client()
        client.connect('localhost', 1883)
        client.loop_start()
        time.sleep(1)
        for x in range(10):
            self.my_data['Time'] = time.asctime()
            client.publish('COMP216/test', json.dumps(self.my_data))
            print('Message sent')
            time.sleep(15)
        client.loop_stop()


pub = Publisher()
pub.start_client()
