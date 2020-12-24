import paho.mqtt.client as mqtt
from gpiozero import OutputDevice
import Adafruit_DHT
import sys
import time

broker = "broker.hivemq.com"
port = 1883
keepalive = 60
relay = OutputDevice(17)

def on_message(client, userdata, message): #for processing subscribed messages
    msg = str(message.payload.decode("utf-8"))
    print("message received ", msg)
    automation(msg)


def automation(msg):


relay = OutputDevice(17)
client = mqtt.Client()
client.on_message = on_message
client.connect(broker, port, keepalive)
client.loop_start()

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11, 4) #type of sensor, GPIO pin
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
        # Send the humidity and temperature data to the Broker
        client.publish('sensor/temp', temperature, 0)
        client.publish('sensor/hum', humidity, 0)
        client.subscribe("automation/bulb1", 0)
        time.sleep(2)
except KeyboardInterrupt:
    pass

client.loop_stop
client.disconnect()
