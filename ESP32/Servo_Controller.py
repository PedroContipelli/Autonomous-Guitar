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

down_angles = [0]  +  [110] * 24  +  [120] * 6
up_angles   = [0]  +  [190] * 24  +  [160] * 6

up_angles[29] = 170

FRET_DOWN, FRET_UP = 110, 190
STRUM_DOWN, STRUM_UP = 120, 160

def main_test():
    alignment()
    # fret_test()
    # strum_test()
    # pass

def servo_write(new_states, old_states):
    for servo in range(1, 31):
        new_state = new_states[servo]
        old_state = old_states[servo]
        
        if new_state != old_state:
            set_servo_state(servo, new_state)
        # No change in STRUM or No change in FRET UP
        elif 25 <= servo <= 30 or new_state == 0:
            idle(servo)
            
    return new_states.copy() # which becomes old_states

def alignment():
    test_range(1, 30, wait_between=0.20, align=True)

def test_range(min, max, wait_between=0.5, align=False):
    for servo in range(min, max+1):
        if not align:
            print(f"DOWN {servo}")
            set_servo_state(servo, 1)
            time.sleep(wait_between)
        print(f"UP {servo}")
        set_servo_state(servo, 0)
        time.sleep(wait_between)
        print(f"RELEASE {servo}\n")
        idle(servo)
    
def idle(servo):
    set_servo_angle(servo, -1)

def set_servo_state(servo, state):
    if state == 1:
        angle = down_angles[servo]
    elif state == 0:
        angle = up_angles[servo]
    else:
        print("ERROR")

    set_servo_angle(servo, angle)

def set_servo_angle(servo, angle):
    port = servo_to_port[servo] - 1
        
    if 0 <= port < 16:
        driver = driver1
    elif 16 <= port < 30:
        driver = driver2
        port = port - 16
    else:
        print(f"Invalid servo index: {servo}")
        return
    
    if angle == -1:
        driver.release(index = port)
    else:
        driver.position(index = port, degrees = angle)

if __name__ == "__main__":
    main_test()