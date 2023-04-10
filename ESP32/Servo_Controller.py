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
driver3 = Servos(i2c, address=0x42)
driver4 = Servos(i2c, address=0x43)

                      # FRETS     # STRUMS
up_angles   = [0]  +  [165] * 24  +  [160] * 6
down_angles = [0]  +  [80] * 24  +  [120] * 6

# Special frets
up_angles[4] += 10
up_angles[9] += 5
up_angles[15] -= 8
up_angles[17] -= 8
down_angles[20] -= 40; up_angles[20] -= 40; # Screwed up glued out of alignment
up_angles[24] += 5


# Special strums
down_angles[26] += 10; up_angles[26] += 10;
down_angles[27] += 8 ; up_angles[27] += 15;
down_angles[28] -= 5 ; up_angles[28] -= 10;
down_angles[29] += 10; up_angles[29] += 18;

def main_test():
    alignment()
    time.sleep(3)
    
    test_range(1,1, wait_between=1.5, repeats=2)
    # pass

def servo_write(servo_states):
    for servo, state in enumerate(servo_states[1:], start=1):
        set_servo_state(servo, state)

def alignment():
    for servo_group in range(1,30,6):
        print(f"UP {servo_group}-{servo_group+5}")
        for servo in range(servo_group, servo_group+6):
            set_servo_state(servo, 0)
        time.sleep(0.50)
        
        print(f"RELEASE {servo_group}-{servo_group+5}\n")
        for servo in range(servo_group, servo_group+6):
            set_servo_state(servo, -1)
        time.sleep(0.10)

def test_range(min, max, wait_between=0.5, align=False, repeats=1):
    for servo in range(min, max+1):
        for repeat in range(repeats):
            print(f"DOWN {servo}")
            set_servo_state(servo, 1)
            time.sleep(wait_between)

            print(f"UP {servo}")
            set_servo_state(servo, 0)
            time.sleep(wait_between)

            print(f"RELEASE {servo}\n")
            set_servo_state(servo, -1)

def all_notes_test(wait_between=3.0):
    strings = [30, 29, 28, 27, 26, 25]
    strum = 1
    for servo in range(1, 24):
        print(f"DOWN {servo}")
        set_servo_state(servo, 1)
        set_servo_state(strings[servo % 6], strum)
        time.sleep(wait_between)

        print(f"UP {servo}")
        set_servo_state(servo, 0)
        time.sleep(wait_between)

        print(f"RELEASE {servo}\n")
        set_servo_state(servo, -1)

        if servo % 6 == 0:
            strum = 1 - strum


def set_servo_state(servo, state):
    if state == -1:
        angle = -1
    elif state == 0:
        angle = up_angles[servo]
    elif state == 1:
        angle = down_angles[servo]
    else:
        print(f"Invalid servo state: {state}")
        print("Should be only -1, 0, or 1")

    set_servo_angle(servo, angle)

def set_servo_angle(servo, angle):
    port = servo_to_port[servo] - 1

    if 0 <= port < 8:
        driver = driver1
    elif 8 <= port < 16:
        driver = driver2
        port -= 8
    elif 16 <= port < 24:
        driver = driver3
        port -= 16
    elif 24 <= port < 30:
        driver = driver4
        port -= 24
    else:
        print(f"Invalid servo index: {servo}")
        print("Should be 1 - 30")
        return

    if angle == -1:
        driver.release(index = port)
    else:
        driver.position(index = port, degrees = angle)

if __name__ == "__main__":
    main_test()