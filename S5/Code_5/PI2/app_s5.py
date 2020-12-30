import wiotp.sdk.application
import json

options = wiotp.sdk.application.parseConfigFile("app_s5.yaml")
client = wiotp.sdk.application.ApplicationClient(options)

def myEventCallback(event):
    str = "Message Received from [%s]: %s"
    print(str % (event.device, json.dumps(event.data)))

def eventPublishCallback():
    print("Message Sent")

client.connect()
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents(typeId="project3", deviceId="rpi", eventId="status")

while True:
    msg = input("Enter the message: ")
    myData={'name' : 'S5', 'MSG' : msg}
    client.publishCommand("project3", "rpi", 'reboot', "json", myData) #, qos=0, onPublish=eventPublishCallback)
