import ujson
import time
import sys
import network
import sh1106
from umqttsimple import MQTTClient
import mqtt_client

class WinterBoot:

    def __init__(self):
        
        self.components = {}
        with open("config.json") as fp:
            data = ujson.loads(fp.read())
        
        if "sensors" in data:
            for sensor in data["sensors"]:
                print(sensor)
                deviceclass = sensor["device_class"]
                name = sensor["name"]
                attributes = sensor["attributes"]

                
                module_obj = __import__(sensor["module"])
                globals()[sensor["module"]] = module_obj
                
                module = getattr(sys.modules[__name__], sensor["module"])
                print(deviceclass, name, attributes, module)

                setattr(self, name, getattr(module, deviceclass)(**attributes))
                
                print(type(getattr(self, name)))
                self.components[name] = getattr(self, name)
        
        if "components" in data:
            for component in data["components"]:
                print(component)
                deviceclass = component["device_class"]
                name = component["name"]
                attributes = component["attributes"]

                
                module_obj = __import__(component["module"])
                globals()[component["module"]] = module_obj
                
                module = getattr(sys.modules[__name__], component["module"])
                print(deviceclass, name, attributes, module)

                setattr(self, name, getattr(module, deviceclass)(**attributes))

            
            
        
        if "winter_blue" in data:
            import __main__
            handler_class = data['winter_blue']['handler_class']
            handler_function = data['winter_blue']['handler_function']
            print(f"{handler_class=}, {handler_function=}")
       
       
            function_name = f"{handler_class}.{handler_function}"
            function_object = eval(function_name)
            
            
            import winter_blue
            print(data["winter_blue"]["name"])
            self.winter_blue = winter_blue.WinterBlue(name = data["winter_blue"]["name"], handler = function_object)
            
        if "sleep" in data:
            self.sleep = data["sleep"]
            
        if "wifi" in data:
            self.__wlan_sta = network.WLAN(network.STA_IF)
            self.__wlan_sta.active(True)
            self.__networks = self.__wlan_sta.scan()
            print(self.__networks)

            self.__wlan_sta.disconnect()
            self.__wlan_sta.connect(data["wifi"]["SSID"], data["wifi"]["password"])
            for retry in range(200):
                connected = self.__wlan_sta.isconnected()
                if connected:
                    break
                time.sleep(0.1)
                print('.', end='')
            if connected:
                print('\nConnected. Network config: ', self.__wlan_sta.ifconfig())
                self.ip = self.__wlan_sta.ifconfig()[3]
                
        if "mqtt" in data:
            self.__mqtt_server = data["mqtt"]["mqtt_server"]
            self.__client_id = data["mqtt"]["client_id"]
            self.__topic = data["mqtt"]["topic"]
            self.__username = data["mqtt"]["username"]
            self.__password = data["mqtt"]["password"]
            self.__port = data["mqtt"]["port"]
            self.__SSL = data["mqtt"]["SSL"]

            
            self.mqtt_client = mqtt_client.mqtt_client(self.__mqtt_server,
                                                       self.__client_id,
                                                       self.__topic,
                                                       self.__username,
                                                       self.__password,
                                                       self.__port,
                                                       self.__SSL)
                                                       


        if "host" in data:
            self.host = data["host"]
            
