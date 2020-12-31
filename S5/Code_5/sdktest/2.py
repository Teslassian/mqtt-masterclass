import wiotp.sdk.application

options = wiotp.sdk.application.parseConfigFile("2.yaml")
client = wiotp.sdk.application.ApplicationClient(options)

def myEventCallback(event):
    str = "Message Received from [%s]: %s"
    print(str % (event.device, json.dumps(event.data)))

client.connect()
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents(typeId=test, deviceId=RPi4, eventId="status", msgFormat='json')
myData={'name' : '2', 'msg' : "Device 2 sent this"}
client.publishEvent(project3, rpi, "status", "json", myData)
