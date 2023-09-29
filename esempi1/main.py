from machine import Pin, Timer, Signal
import machine
import socket
import _thread
import json
import time

JSON_FILE = 'gate96.json'
# variabili
# where + type + object_name
# type: b=boolean; i=integer; f=float; s=string; t=timer 
# where: i=in; o=out; s=static
# ib_p1_on
# if_p1_current
# sb_alarm_p1_current
pin_ls_opened = Pin(12, Pin.IN, Pin.PULL_UP) # na: quando True sensore impegnato ferma movimento
pin_ls_closed = Pin(13, Pin.IN, Pin.PULL_UP) # na: quando True sensore impegnato ferma movimento
pin_ls_safety = Pin(15, Pin.IN, Pin.PULL_UP) # nc: quando False consenso movimento
pin_pls_toggle = Pin(0, Pin.IN, Pin.PULL_UP)
pin_out_open = Signal(14, Pin.OUT, invert = True) # 
pin_out_close = Signal(2, Pin.OUT, invert = True)
pin_out_light = Signal(16, Pin.OUT, invert = False)
#GPIO4 reserved for future bluetooth and flash
timer_out = Timer(0)
TIMER_OUT_PERIOD = 10000
ob_open = False
ob_close = False

def render_html(file_name):
    f = open(file_name,"rb")
    ret = f.read()
    f.close
    return ret

def ls_event(pin):
    print('pin event')
    if pin.value():
        set_mov(False, False)
	
pin_ls_opened.irq(trigger=Pin.IRQ_RISING, handler=ls_event)
pin_ls_closed.irq(trigger=Pin.IRQ_RISING, handler=ls_event)
pin_ls_safety.irq(trigger=Pin.IRQ_RISING, handler=ls_event)
pin_pls_toggle.irq(trigger=Pin.IRQ_FALLING, handler= lambda pin:- toggle_mov())
#pin_ls_safety.irq(trigger=Pin.IRQ_RISING, handler= lambda pin:- set_mov(false, false))
print('pins configured')

def toggle_mov():
    if not ob_close or not ob_open:
        print("toggle to stop")
        set_mov(False, False)
    elif pin_ls_opened.value() and not pin_ls_closed.value():
        print("toggle to close")
        set_mov(False, True)
    elif not pin_ls_opened.value():
        print("toggle to open")
        set_mov(True, False)
    else:
        print("toggle .....")
        set_mov(False, False)
        
def set_mov(open = False, close = False):
    global ob_close, ob_open
    if pin_ls_safety.value():
        print("Set_mov safety stop")
        pin_out_open.off()
        ob_open = False
        pin_out_close.off()
        ob_close = False
        pin_out_light.off()
        return
    if open and not pin_ls_opened.value():
        print("Set_mov open")
        pin_out_open.on()
        ob_open = True
        timer_out.init(period=TIMER_OUT_PERIOD, mode=Timer.ONE_SHOT, callback= lambda t: set_mov())
    else:
        print("Set_mov open stop")
        pin_out_open.off()
        ob_open = False
    ###
    if close and not pin_ls_closed.value():
        print("Set_mov close")
        pin_out_close.on()
        ob_close = True
        timer_out.init(period=TIMER_OUT_PERIOD, mode=Timer.ONE_SHOT, callback= lambda t: set_mov())
    else:
        print("Set_mov close stop")
        pin_out_close.off()
        ob_close = False
    ###
    if open or close:
        pin_out_light.on()
    else:
        pin_out_light.off()

def load_data():
    global TIMER_OUT_PERIOD
    print('load data')
    try:
        with open(JSON_FILE) as json_file:
            data = json.load(json_file)
            print(data)
        TIMER_OUT_PERIOD = data['timer_out_period']
    except:
        print('error to load json data')

def save_data():
    data = {
        'timer_out_period':TIMER_OUT_PERIOD
        }
    with open(JSON_FILE, 'w') as outfile:
        json.dump(data, outfile)
    print('save data')
    print(data)

def webThread():
    global TIMER_OUT_PERIOD
    i = 0
    while True:
        try:
            conn, addr = s.accept() 
            print("web request:")
            request = str(conn.recv(1024))
            cmnd = request.split(' ',)[1]
            print("Command:", cmnd)
            response = ''
            if cmnd == "/open":
                set_mov(True, False)
                response = render_html('home.html')
                conn.sendall(response)
                conn.close()
            elif cmnd == "/close":
                set_mov(False, True)
                response = render_html('home.html')
                conn.sendall(response)
                conn.close()
            elif cmnd == "/stop":
                set_mov(False, False)
                response = render_html('home.html')
                conn.sendall(response)
                conn.close()
            elif cmnd == "/w3.css" or cmnd == "/favicon.png":
                response = render_html(cmnd[1:])
                conn.sendall(response)
                conn.close()
            elif cmnd == "/get_values":
                response = json.dumps({
                    'time': time.time(),
                    'ls_opened': pin_ls_opened.value(),
                    'ls_closed': pin_ls_closed.value(),
                    'ls_safety': pin_ls_safety.value(),
                    'out_open': ob_open,
                    'out_close': ob_close,
                    'timer_out_period': TIMER_OUT_PERIOD
                })
                print(response)
                conn.sendall(response.encode())
                conn.close()
            elif cmnd[:14]=='/plc_set_value':
                args = cmnd.split('%')[1].split('=')
                if args[0] == 'timer_out_period':
                    TIMER_OUT_PERIOD = int(args[1])
                    print('salvato timer_out_period')
                    save_data()
                response = render_html('home.html')
                conn.sendall(response)
                conn.close()
            else:
                response =render_html('home.html')
                conn.sendall(response)
                conn.close()
            print("Request executed")
        except:
            i += 1
            if i > 75:
                i = 0
                print(time.time(),"no request")

load_data()
set_mov(False, False)
# prepare socket listener
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(4)
s.bind(('', 80))
s.listen(2)
_thread.start_new_thread(webThread, ())
