import wiotp.sdk.application

options = wiotp.sdk.application.parseConfigFile("1.yaml")
client = wiotp.sdk.application.ApplicationClient(options)

def myEventCallback(event):
    str = "Message Received from [%s]: %s"
    print(str % (event.device, json.dumps(event.data)))

client.connect()
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents(typeId=project3, deviceId=rpi, eventId="status", msgFormat='json')
myData={'name' : '1', 'msg' : "Device 1 sent this"}
client.publishEvent(test, RPi4, "status", "json", myData)
