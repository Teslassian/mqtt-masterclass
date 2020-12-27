import wiotp.sdk.device
from gpiozero import OutputDevice
import adafruit_dht
import board
import json
import time
import sys

# Variables
relay = OutputDevice(17)

# Configure
options = wiotp.sdk.device.parseConfigFile("device.yaml")
client = wiotp.sdk.device.DeviceClient(options)
client.commandCallback = myCommandCallback

# Callback Function for published data
def eventPublishCallback():
    print("Device Publish Event done!!!")

# Callback Function for received commands
def myCommandCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))
    msg = str(json.dumps(event.data))
    automation(msg)






# Function for processing subscribed messages
def on_message(client, userdata, message): #forprocessingsubscribedmessages
    msg = str(message.payload.decode("utf-8"))
    print("message received ", msg)
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
        client.publishEvent(eventId="temp", msgFormat="json", data=temperature, qos=0, onPublish=eventPublishCallback)
        client.publishEvent(eventId="hum", msgFormat="json", data=humidity, qos=0, onPublish=eventPublishCallback)
        time.sleep(2)
    except RuntimeError as error:
        print(error.args[0])

# Cleanup
client.loop_stop()
client.disconnect()
