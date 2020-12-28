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
    print("Device Publish Event done!!!")

# Callback Function for messages received from the device
def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)
    # str = "%s event '%s' received from device [%s]: %s"
    # print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))
    msg = str(json.dumps(cmd.data))
    automation(msg)

# Function for controlling the relay
def automation(msg):
    if msg == "on":
        relay.on()
    elif msg == "off":
        relay.off()
    else:
        relay.off()
        print("Invalid Message")

# Configure
options = wiotp.sdk.device.parseConfigFile("rpi.yaml")
client = wiotp.sdk.device.DeviceClient(options)
client.myCommandCallback = myCommandCallback

# Connect
client.connect()

# # Subscribe - devices automatically subscribe?
# client.subscribeToDeviceEvents()

# DHT
dhtDevice = adafruit_dht.DHT11(board.D4)

# Main loop
while True:
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        humidity = round(humidity, 3)
        temperature = round(temperature, 3)
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        myData1 = {'temperature': temperature}
        myData2 = {'humidity': humidity}
        client.publishEvent(eventId="temp", msgFormat="json", data=myData1, qos=2, onPublish=eventPublishCallback)
        client.publishEvent(eventId="hum", msgFormat="json", data=myData2, qos=2, onPublish=eventPublishCallback)
        time.sleep(2)
    except RuntimeError as error:
        print(error.args[0])

mqttc.loop_forever()
