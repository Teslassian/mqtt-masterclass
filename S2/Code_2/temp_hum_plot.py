import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('temp_hum.csv', delimiter=",", names=["time", "temperature", "humidity"])
plt.plot(data['time'], data['temperature'])
plt.plot(data['time'], data['humidity'])
plt.legend(['temperature (deg C)', 'humidity (%)'])
plt.xlabel('time')
plt.show()
