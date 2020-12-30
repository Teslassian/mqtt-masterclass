import wiotp.sdk.device
import json

options = wiotp.sdk.device.parseConfigFile("dev_rpi.yaml")
client = wiotp.sdk.device.DeviceClient(options)

def myCommandCallback(cmd):
    str = "Message Received: %s"
    print(str % (cmd.data))

def eventPublishCallback():
    print("Message Sent")

client.connect()
client.commandCallback = myCommandCallback

while True:
    msg = input("Enter the message: ")
    myData={'name' : 'Naveen', 'MSG' : msg}
    client.publishEvent(eventId='status', msgFormat='json', data=myData, qos=0, onPublish=eventPublishCallback)
