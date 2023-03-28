try:
    import usocket as socket
except:
    import socket
    
from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'intanetalctsa'
password = '4074062466'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())