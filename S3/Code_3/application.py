import wiotp.sdk.application
import json
from gpiozero import OutputDevice
import adafruit_dht
import board
import sys
import time
# import paho.mqtt.client as mqtt
# import csv

# Initialization of variables
broker = "192.168.137.1"
port = 1883
keepalive = 60
relay = OutputDevice(17)

# Initialization of the IBM Cloud interaction
options = wiotp.sdk.application.parseConfigFile("app.yaml")
client = wiotp.sdk.application.ApplicationClient(options)

def myEventCallback(event):
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

# Initialization of MQTT client
client = mqtt.Client()
client.on_message = on_message
client.connect(broker, port, keepalive)
client.loop_start()

# Initialization of the IBM cloud connection
client.connect()
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents(typeId="test", deviceId="device1", eventId="status1")

# Initialization of DHT device
dhtDevice = adafruit_dht.DHT11(board.D4)

# Main loop
i = 0;
while True:
    try:
        # humidity, temperature = Adafruit_DHT.read_retry(11, 4)  #sensor, gpio
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        # Sending humidity and temperature data to Broker
        client.publish('sensor/temp',temperature, 0)
        client.publish('sensor/hum',humidity, 0)
        client.subscribe("automation/bulb1", 0)
        # Write data to csv file
        with open('temp_hum.csv', mode='a') as file:
            file.write(str(i) + ',' +  str(temperature) + ',' + str(humidity) + '\n')
            # file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # file_writer.writerow([i, temperature, humidity])
        i += 2
        time.sleep(2)
    except RuntimeError as error:
        print(error.args[0])

# Cleanup
client.loop_stop()
client.disconnect()
