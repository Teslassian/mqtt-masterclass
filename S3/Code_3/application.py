import wiotp.sdk.application
from gpiozero import OutputDevice
import adafruit_dht
import board
import json
import sys
import time

# Variables
relay = OutputDevice(17)

# Configure
options = wiotp.sdk.application.parseConfigFile("application.yaml")
client = wiotp.sdk.application.ApplicationClient(options)

# Callback Function for messages received from the device
def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))
    msg = str(json.dumps(event.data))
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

# Connect
client.connect()
client.deviceEventCallback = myEventCallback

# Subscribe - check this
client.subscribeToDeviceEvents()
