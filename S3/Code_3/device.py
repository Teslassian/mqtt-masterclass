import wiotp.sdk.device
import adafruit_dht
import board
import time
import sys

# Configure
options = wiotp.sdk.device.parseConfigFile("device.yaml")
client = wiotp.sdk.device.DeviceClient(options)

# Callback Function for published data
def eventPublishCallback():
    print("Device Publish Event done!!!")

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
        myData1 = {'temperature': temperature}
        myData2 = {'humidity': humidity}
        client.publishEvent(eventId="temp", msgFormat="json", data=myData1, qos=2, onPublish=eventPublishCallback)
        client.publishEvent(eventId="hum", msgFormat="json", data=myData2, qos=2, onPublish=eventPublishCallback)
        time.sleep(2)
    except RuntimeError as error:
        print(error.args[0])

mqttc.loop_forever()
