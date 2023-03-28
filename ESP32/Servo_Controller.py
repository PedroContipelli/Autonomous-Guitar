# https://learn.adafruit.com/micropython-hardware-pca9685-pwm-and-servo-driver/circuitpython#dim-leds
if __name__ == "__main__":
    import uos
    uos.chdir('ESP32')

from LookupTables import servo_to_port
from machine import Pin, SoftI2C
import time
from servo import Servos

# initialize i2c object
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# initialize pca9685 drivers
driver1 = Servos(i2c, address=0x40)
driver2 = Servos(i2c, address=0x41)

FRET_DOWN, FRET_UP = 110, 190
STRUM_DOWN, STRUM_UP = 120, 160

def main_test():
    fret_test()
        
def strum_test():
    for strum in range(25,31):
        print(f"STRUM DOWN {strum}")
        set_servo_angle(strum, STRUM_DOWN)
        time.sleep(1)
        print(f"STRUM UP {strum}")
        set_servo_angle(strum, STRUM_UP)
        time.sleep(1)
        print(f"RELEASE {strum}")
        set_servo_angle(strum, -1)
        time.sleep(1)
        
def fret_test():
    for fret in range(17,19):
        print(f"FRET DOWN {fret}")
        set_servo_angle(fret, FRET_DOWN)
        time.sleep(0.5)
        print(f"FRET UP {fret}")
        set_servo_angle(fret, FRET_UP)
        time.sleep(0.5)
        print(f"RELEASE {fret}")
        set_servo_angle(fret, -1)
    

def set_servo_angle(servo, degrees):
    port = servo_to_port[servo] - 1
        
    if 0 <= port < 16:
        driver = driver1
    elif 16 <= port < 30:
        driver = driver2
        port = port - 16
    else:
        print(f"Invalid servo index: {servo}")
        return
    
    if degrees == -1:
        driver.release(index = port)
    else:
        driver.position(index = port, degrees = degrees)

if __name__ == "__main__":
    main_test()

