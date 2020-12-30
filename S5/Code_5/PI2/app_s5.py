import wiotp.sdk.application
import json
options = wiotp.sdk.application.parseConfigFile("app_s5.yaml")
client = wiotp.sdk.application.ApplicationClient(options)

def myEventCallback(event):
    str = "Message Received from [%s]: %s"
    print(str % (event.device, json.dumps(event.data)))

def eventPublishCallback():
    print("Message Sent")

while True:
    client.connect()
    client.deviceEventCallback = myEventCallback
    client.subscribeToDeviceEvents(typeId="project3", deviceId="rpi", eventId="status2")
    msg = input(" ")
    myData={'name' : 'S5', 'MSG' : msg}
    client.publishEvent(typeId="project3", deviceId="rpi", eventId="status1", msgFormat="json", data=myData) #, qos=0, onPublish=eventPublishCallback)
