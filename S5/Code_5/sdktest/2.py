import wiotp.sdk.application

options = wiotp.sdk.application.ParseConfigFile("2.yaml")
client = wiotp.sdk.application.ApplicationClient(options)

def myEventCallback(event):
    str = "Message Received from [%s]: %s"
    print(str % (event.device, json.dumps(event.data)))

client.connect()
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents(typeId=rpi1, deviceId=sdktest1, eventId="status", msgFormat='json')
myData={'name' : '2', 'msg' : "Device 2 sent this"}
client.publishEvent(rpi2, sdktest2, "status", "json", myData)
