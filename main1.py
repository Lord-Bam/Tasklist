#https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/
import winterboot
import __main__
import time
import machine
import sh1106
import json
import ntptime
from machine import deepsleep
from time import sleep
import taskserver
import uasyncio as asyncio


wb = winterboot.WinterBoot()

asyncio.run(taskserver.start_web_server())

while True:
    time.sleep(1)
    print("done")