
# This file is executed on every boot (including wake-boot from deepsleep)
import esp
#esp.osdebug(None)
import uos
#uos.dupterm(None, 1) # disable REPL on UART(0)
import webrepl
import gc
import network
#from umqttsimple import MQTTClient

webrepl.start()
gc.collect()

SSID = 'Gate96-AP'
SSID_PW = 's16a7e20s16a7'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(authmode=3,essid=SSID, password=SSID_PW)
while ap.active() == False:
    pass
print('Connection successful')
print(ap.ifconfig())

