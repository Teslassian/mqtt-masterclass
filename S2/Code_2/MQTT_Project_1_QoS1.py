import paho.mqtt.client as mqtt
from gpiozero import OutputDevice
import Adafruit_DHT
import sys
import time
import board

# Initialization of variables
broker="192.168.137.1"
port =1883
keepalive=60
relay = OutputDevice(17)

# Function for processing subscribed messages
def on_message(client, userdata, message): #forprocessingsubscribedmessages
    msg = str(message.payload.decode("utf-8"))
    print("message received " ,msg)
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

# Initialization of MQTT Client
client = mqtt.Client()
client.on_message = on_message
client.connect(broker, port, keepalive)
client.loop_start()

# Initialization of DHT device
dhtDevice = adafruit_dht.DHT11(board.D4)

# Main loop
try:
    while True:
        # humidity, temperature = Adafruit_DHT.read_retry(11, 4)  #sensor, gpio
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        # Sending humidity and temperature data to Broker
        client.publish('sensor/temp',temperature, 1)
        client.publish('sensor/hum',humidity, 1)
        client.subscribe("automation/bulb1", 1)
        time.sleep(2)
except KeyboardInterrupt:
    pass

# Cleanup
client.loop_stop()
client.disconnect()
