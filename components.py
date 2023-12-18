import machine
import ds18x20
import onewire
import time
import neopixel
import dht
import sh1106


class WinterPin(machine.Pin):
    
    def __init__(self, pin, mode):
        if mode == "in":
            super().__init__(pin, machine.Pin.IN)
        elif mode == "out":
            super().__init__(pin, machine.Pin.OUT)

       
class Oled():
    
    def __init__(self, scl, sda):
        self.__i2c = machine.I2C(scl=machine.Pin(scl), sda=machine.Pin(sda), freq=400000)
        self.__display = sh1106.SH1106_I2C(128, 64, self.__i2c, machine.Pin(16), 0x3C, rotate=180)
        self.__display.sleep(False)
        self.__lines = [""] * 5
        self.__display.fill(0)
    
    
    def write_line(self, line_number, text):
        self.__display.fill(0)
        self.__lines[line_number] = text
        for x in range(0,4):
            self.__display.text(self.__lines[x], 0, x * 10, 1)
        self.__display.show()

            
            
class DHT11():
    
    def __init__(self, pin):
        self.__sensor = dht.DHT11(machine.Pin(19))
        
    def measure(self):
        time.sleep(0.3)
        try:
            self.__sensor.measure()
            return self.__sensor.temperature(), self.__sensor.humidity()
        except OSError as e:
            print('Failed to read sensor.')
            return None
        
class DHT11_temp(DHT11):
    
    def __init__(self, pin):
         super().__init__(pin)
         
    def measure(self):
        time.sleep(0.3)
        try:
            self.__sensor.measure()
            return self.__sensor.temperature()
        except OSError as e:
            print('Failed to read sensor.')
            return None
    
class DHT11_hum(DHT11):
    
    def __init__(self, pin):
         super().__init__(pin)
         
    def measure(self):
        time.sleep(0.3)
        try:
            self.__sensor.measure()
            return self.__sensor.humidity()
        except OSError as e:
            print('Failed to read sensor.')
            return None

class VoltageMeter():
    
    def __init__(self, pin, voltage_devider = False):
        self._meter = machine.ADC(machine.Pin(pin))
        #set max voltage to 2.45V
        self._meter.atten(machine.ADC.ATTN_11DB)
        self._voltage_devider = voltage_devider
        
        
    def measure(self):
        result = self._meter.read_uv() / 1000000
        
        if self._voltage_devider == True:
            return result * 2
        else:
            return result
    
class Led(machine.Pin):

    def __init__(self, pin):    
        super().__init__(pin, machine.Pin.OUT)
        
    def on(self):
        self.value(1)
        
    def off(self):
        self.value(0)
        
    def toggle(self):
        if self.value() == 0:
            self.value(1)
        else:
            self.value(0)
            
    def state(self):
        return self.value()
        
class Joystick():
    
    def __init__(self, x, y, sw=None):
        self.x = machine.ADC(machine.Pin(39))          # create ADC object on ADC pin
        self.x.atten(machine.ADC.ATTN_11DB)    # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        self.x.width(machine.ADC.WIDTH_9BIT)   # set 9 bit return values (returned range 0-511)


        self.y = machine.ADC(machine.Pin(36))          # create ADC object on ADC pin
        self.y.atten(machine.ADC.ATTN_11DB)    # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        self.y.width(machine.ADC.WIDTH_9BIT)   # set 9 bit return values (returned range 0-511)
            
    def read(self):
        return self.x.read(), self.y.read()
    
class NeoPixel(neopixel.NeoPixel):
    
    def __init__(self, pin):
        neo_pixel_pin = machine.Pin(pin, machine.Pin.OUT)
        super().__init__(neo_pixel_pin, pin)
 
 

        
    

        
        
    
 
 
 
###########################
# Still needs refactoring #
###########################

        
class Temp_sensor:
    
    def __init__(self, args):
        print("constructor")
        _ds_pin = machine.Pin(args["pin"])
        self._ds_sensor = ds18x20.DS18X20(onewire.OneWire(_ds_pin))
        _roms = self._ds_sensor.scan()
        print("Found DS devices: ", _roms)
        self._rom = _roms[0]
        
        
    def read_temp(self):
        self._ds_sensor.convert_temp() #needs to be done everytime you read a value.
        current_temp = self._ds_sensor.read_temp(self._rom)
        return current_temp

class Button():
    #https://docs.micropython.org/en/latest/library/machine.Pin.html
    #https://docs.micropython.org/en/latest/reference/isr_rules.html#isr-rules
    #
    
    def interrupt_handler(self, pin):
        if self.debouncer + 30 < time.ticks_ms():
            time.sleep(0.01)
            self.debouncer = time.ticks_ms()
            self.value = pin.value()
            self.interrupt = True
    
    def __init__(self, pin):
        self.debouncer = time.ticks_ms()
        button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        button.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=self.interrupt_handler)
        self.value = button.value()
        self.interrupt = False
        
    @property
    def getvalue(self):
        return self.value
    
    def get_interrupt(self):
        return_value =  self.interrupt
        self.interrupt = False
        return return_value 

        