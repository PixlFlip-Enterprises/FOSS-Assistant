# Once active run forever a set of all sensors connected to the device and store the data for easy retrieval
"""Super primitive for now but will systematically post latest information to database for other functions to use."""
import Adafruit_DHT
sensor = Adafruit_DHT.DHT11
pin = 4
while True:
     humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
     print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
