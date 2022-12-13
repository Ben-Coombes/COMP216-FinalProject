import paho.mqtt.client as mqtt

client = mqtt.Client() #instantiates a client
client.connect('localhost', 1883) #connects to the server
client.publish('COMP216', payload='Hello from Narendra')
client.disconnect()