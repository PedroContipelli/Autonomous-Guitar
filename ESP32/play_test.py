import time
from machine import Pin
abort = Pin(0, Pin.IN)
stop = False
halt = 0
def abortPlay(pin):
    global stop
    stop = True
def changeStop():
    global stop
    stop = False
def main(decision):
    while True:
        print(decision)
        time.sleep(1)
        print(stop)
        if stop:
            print("interrupt")
            changeStop()
            break


abort.irq(trigger=Pin.IRQ_FALLING, handler = abortPlay)