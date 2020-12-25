client = paho.Client()

client.on_message = on_message

client.connect(host, 1883)

client.subscribe("SYS/#", qos=1)

# pseudocode start

def wait_for_data():

...

msg = wait_for_data()

client.publish("SYS/reported/", msg, qos=1)

# pseudocode end

client.loop_forever()
