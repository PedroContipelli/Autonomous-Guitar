import uos
uos.chdir('ESP32')

from LookupTables import physical_map
from machine import Pin
import time

led = Pin(2, Pin.OUT)
SER = Pin(0, Pin.OUT)
RCLK = Pin(4, Pin.OUT)
SRCLK = Pin(16, Pin.OUT)

num_servos = 30
virtual_states = [0 for _ in range(num_servos + 1)]
cycles = 50
extra_wait_time = 0.20 # in seconds

def main_test():
    # Resets to starting position
    alignment()

    # Test all in this range (inclusive)
    test_range(min=1, max=30, reps=3)

    # FOR MAPPING:
    # Run test_range() with reps=3 and write down sequence of which physical
    # servos are played in left column of "physical_map" in LookupTables.py

# Set all to 0 or 1
def alignment(set_to=0):
    virtual_states = [set_to for _ in range(num_servos + 1)]
    servo_write(virtual_states)
    time.sleep(extra_wait_time)

# Counts up powering each servo ON and OFF once
def test_range(min=1, max=num_servos, reps=1):
    for servo in range(min, max + 1):
      for _ in range(reps):
          print(f"Servo #{servo} ON\n")
          virtual_states[servo] = 1
          servo_write(virtual_states)
          time.sleep(extra_wait_time)

          print(f"Servo #{servo} OFF\n")
          virtual_states[servo] = 0
          servo_write(virtual_states)
          time.sleep(extra_wait_time)

def output(value):
  SER.value(value)

def shift(n):
  for i in range(n):
    SRCLK.value(1)
    SRCLK.value(0)

def store():
  RCLK.value(1)
  RCLK.value(0)

def servo_write(servo_states):
  # incoming servo_states is 1-indexed for physical convention reasons
  num_servos = len(servo_states) - 1

  for _ in range(cycles):
    min_angle = 100
    max_angle = 500

    output(1)
    shift(num_servos)
    store()
    time.sleep_us(min_angle)

    # Serial data loaded in from front to back (reverse order)
    for virtual_servo in range(num_servos, 0, -1):
      # Allows adaptability to physical wiring changes
      true_servo = physical_map[virtual_servo]
      output(1 - servo_states[true_servo])
      shift(1)

    store()
    time.sleep_us(max_angle - min_angle)

    output(0)
    shift(num_servos)
    store()
    time.sleep_us(20_000 - max_angle)

if __name__ == "__main__":
    main_test()
