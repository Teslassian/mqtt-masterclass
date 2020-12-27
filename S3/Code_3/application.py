import wiotp.sdk.application
import json

# Configure
options = wiotp.sdk.application.parseConfigFile("app.yaml")
client = wiotp.sdk.application.ApplicationClient(options)

# Callback function for received messages
def myEventCallback(event):
    str = "Message received from [%s]: %s"
    print(str % (event.device, json.dumps(event.data)))

# Connect
client.connect()
client.deviceEventCallback = myEventCallback

while True:
    
