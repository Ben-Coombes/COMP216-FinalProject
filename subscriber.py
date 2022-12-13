import paho.mqtt.client as mqtt
import json


# this function is called when the subscriber receives a message
# we are simply display some data items on screen, normally this
# data is sent to another system to be cleansed, stored and processed
# and then some action can be taken
def on_message(client, userdata, message):
    data = message.payload.decode('utf-8')
    obj = json.loads(data)
    print(f'Blood Pressure @ Time: {obj["Time"]}')
    print(f'{obj["BloodPressure"]["Diastolic"]}(dia)', end=' ')
    print(f'{obj["BloodPressure"]["Systolic"]}(sys) ')


client = mqtt.Client()
client.on_message = on_message
client.connect('localhost', 1883)
client.subscribe('COMP216/test')
while True:
    client.loop_forever()
