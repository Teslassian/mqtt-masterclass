import wiotp.sdk.device
import json
options = wiotp.sdk.device.parseConfigFile("rpi.yaml")
client = wiotp.sdk.device.DeviceClient(options)

def myEventCallback(event):
    str = "Message Received from [%s]: %s"
    print(str % (event.device, json.dumps(event.data)))

def eventPublishCallback():
    print("Message Sent")

client.connect()
client.deviceEventCallback = myEventCallback

while True:
    client.subscribeToDeviceEvents(typeId="project3", deviceId="client1", eventId="status1")
    msg = input(" ")
    myData={'name' : 'Naveen', 'MSG' : msg}
    client.publishEvent(typeId="project3", deviceId="client2", eventId="status2", msgFormat="json", data=myData, qos=0, onPublish=eventPublishCallback)
