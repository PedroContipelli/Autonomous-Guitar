if __name__ == "__main__":
    import uos
    uos.chdir('ESP32')

from LookupTables import servo_to_port
from machine import Pin, SoftI2C
import time
from Libraries.servo import Servos

# initialize i2c object
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# initialize pca9685 drivers
driver1 = Servos(i2c, address=0x40)
driver2 = Servos(i2c, address=0x41)

                      # FRETS     # STRUMS
up_angles   = [0]  +  [170] * 24  +  [160] * 6
down_angles = [0]  +  [80] * 24  +  [120] * 6

# Special frets
up_angles[18] = 190
up_angles[3] = 190
down_angles[1] = 80
down_angles[7] = 80

# Special strums
up_angles[29] = 170

# FRET_DOWN, FRET_UP = 110, 190
# STRUM_DOWN, STRUM_UP = 120, 160

def main_test():
    # alignment()
    test_range(17,30)
    # pass

def servo_write(servo_states):
    for servo, state in enumerate(servo_states[1:], start=1):
        set_servo_state(servo, state)

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
        set_servo_state(servo, -1)

def set_servo_state(servo, state):
    if state == -1:
        angle = -1
    elif state == 0:
        angle = up_angles[servo]
    elif state == 1:
        angle = down_angles[servo]
    else:
        print(f"Invalid servo state: {state}")

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