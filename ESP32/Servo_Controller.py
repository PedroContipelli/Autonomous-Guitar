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
previous_states = [0 for _ in range(num_servos + 1)]
cycles = 20
extra_wait_time = 0.1 # in seconds

def main_test():
    # Resets to starting position
    alignment()

    # Test all in this range (inclusive)
    while True:
        test_range(min=1, max=30, reps=1)

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
    min_angle = 150 # microseconds
    max_angle = 450 # microseconds
        
    # Controls whether servo is operating or completely OFF
    for virtual_servo in range(num_servos, 0, -1):
      # Allows adaptability to physical wiring changes
      true_servo = physical_map[virtual_servo]
      
      prev_state = previous_states[true_servo]
      current_state = servo_states[true_servo]
      
      # We only want servo to be COMPLETELY OFF after it has already unfretted
      output(prev_state or current_state)
      shift(1) # Only shifting a single bit into one servo
    store()
    time.sleep_us(min_angle)

    # Serial data loaded in from front to back (reverse order)
    for virtual_servo in range(num_servos, 0, -1):
      # Allows adaptability to physical wiring changes
      true_servo = physical_map[virtual_servo]
      
      prev_state = previous_states[true_servo]
      current_state = servo_states[true_servo]
      
      # We only want servo to FRET UP if previous state was fret down
      output((not current_state) and prev_state)
      
      shift(1) # Only shifting a single bit into one servo
    store()
    time.sleep_us(max_angle - min_angle)

    output(0)
    shift(num_servos) # Shifting 0 into ALL servos
    store()
    time.sleep_us(20_000 - max_angle)
    
  # Python does not like previous_states = servo_states.copy() because it thinks prev_states is local variable
  for i in range(num_servos + 1):
      previous_states[i] = servo_states[i]

if __name__ == "__main__":
    main_test()
