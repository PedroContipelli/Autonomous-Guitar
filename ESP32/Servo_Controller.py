from LookupTables import physical_map
from machine import Pin
import time

led = Pin(2, Pin.OUT)
SER = Pin(0, Pin.OUT)
RCLK = Pin(4, Pin.OUT)
SRCLK = Pin(16, Pin.OUT)
cycles = 10

def main_test():
    num_servos = 30
    virtual_states = [0 for _ in range(num_servos + 1)]
    wait_time = 0.20

    # Reset to starting position
    servo_write(virtual_states)
    time.sleep(wait_time)

    # Counts up powering ON and OFF each servo once
    for servo in range(num_servos):
      print(f"Servo #{servo} ON\n")
      virtual_states[servo] = 1
      servo_write(virtual_states)
      time.sleep(wait_time)

      print(f"Servo #{servo} OFF\n")
      virtual_states[servo] = 0
      servo_write(virtual_states)
      time.sleep(wait_time)

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
