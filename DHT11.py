# Complete project details at https://RandomNerdTutorials.com
from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(19))

while True:
    time.sleep(2)
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print(sensor.temperature())
        print(sensor.humidity())
    except OSError as e:
        print('Failed to read sensor.')


