import wiotp.sdk.device
from gpiozero import OutputDevice
import adafruit_dht
import board
import json
import time
import sys

# Variables
relay = OutputDevice(17)

# Callback Function for published data
def eventPublishCallback():
    print("Data published successfully!")

# Function for controlling the delay
def automation(msg):
    if msg == 'on':
        relay.on()
    elif msg == 'off':
        relay.off()
    else:
        relay.off()
        print("Invalid Message")

# Configure
myConfig = wiotp.sdk.device(parseConfigFile("ass3.yaml"))
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)

# Connect
client.connect()

# DHT11
dhtDevice = adafruit_dht.DHT11(board.D4)

while True:
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        temperature = round(temperature, 3)
        humidity = round(humidity, 3)
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        if temperature >= 31:
            automation('on')
        if temperature <= 29:
            automation('off')
        myData1 = {'temperature': temperature}
        myData2 = {'humidity': humidity}
        client.publishEvent(eventId='temp', msgFormat='json', data=myData1, qos=2, onPublish=eventPublishCallback)
        client.publishEvent(eventId='temp', msgFormat='json', data=myData1, qos=2, onPublish=eventPublishCallback)
        time.sleep(2)
    except RuntimeError as error:
        print(error.args[0])

mqttc.loop_forever()
