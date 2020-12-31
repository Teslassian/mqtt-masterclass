import wiotp.sdk.application

options = wiotp.sdk.application.ParseConfigFile("1.yaml")
client = wiotp.sdk.application.ApplicationClient(options)

def myEventCallback(event):
    str = "Message Received from [%s]: %s"
    print(str % (event.device, json.dumps(event.data)))

client.connect()
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents(typeId=rpi2, deviceId=sdktest2, eventId="status", msgFormat='json')
myData={'name' : '1', 'msg' : "Device 1 sent this"}
client.publishEvent(rpi1, sdktest1, "status", "json", myData)
