if __name__ == "__main__":
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

def main_test():
    # mapping()
    alignment()

    test_range_loop(min=25, max=30, reps=1, wait_time=0.30, cycles=20)
        
def alignment(at_a_time=3):
    virtual_states = [0 for _ in range(num_servos + 1)]
    previous_states = virtual_states.copy()
    
    for servo in range(1, num_servos, at_a_time):
        print(f"Aligning Servos #{servo} - {servo + at_a_time - 1}") 
        for s in range(servo, servo + at_a_time):
            previous_states[s] = 1
        previous_states = servo_write(virtual_states, previous_states, cycles=10)
        time.sleep(0.15)
    
def mapping():
    test_range_loop(reps=3, wait_time=1, cycles=10)

# Counts up powering each servo ON and OFF once
def test_range_loop(min=1, max=30, reps=1, wait_time=0.5, cycles=15):
    while True:
        virtual_states = [0 for _ in range(num_servos + 1)]
        previous_states = virtual_states.copy()
        
        for servo in range(min, max + 1):
          for _ in range(reps):
              print(f"Servo #{servo} ON\n")
              virtual_states[servo] = 1
              previous_states = servo_write(virtual_states, previous_states, cycles=cycles)

              print(f"Servo #{servo} OFF\n")
              virtual_states[servo] = 0
              previous_states = servo_write(virtual_states, previous_states, cycles=cycles)
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

def servo_write(servo_states, previous_states, cycles=15):
  # incoming servo_states is 1-indexed for physical convention reasons
  num_servos = len(servo_states) - 1
  fret_min_angle = 300 # microseconds (smaller = fret lower)
  fret_max_angle = 500 # microseconds (larger = unfret higher)
  strum_min_angle = 300 # currently not doing anything...
  strum_max_angle = 500 # currently not doing anything...

  for _ in range(cycles):
    # Controls whether servo is operating or completely OFF
    for virtual_servo in range(num_servos, 0, -1):
      # Allows adaptability to physical wiring changes
      true_servo = physical_map[virtual_servo]
      
      prev_state = previous_states[true_servo]
      new_state = servo_states[true_servo]
      
      # Strumming servos only powered ON whenever there's a change in state
      if 25 <= virtual_servo <= 30:
          output(prev_state ^ new_state)
      # Fretting servos only powered OFF when remaining in the up position
      else:
          output(prev_state or new_state)

      shift(1) # Only shifting a single bit into one servo
    store()
    time.sleep_us(fret_min_angle)

    # Serial data loaded in from front to back (reverse order)
    for virtual_servo in range(num_servos, 0, -1):
      # Allows adaptability to physical wiring changes
      true_servo = physical_map[virtual_servo]
      
      prev_state = previous_states[true_servo]
      new_state = servo_states[true_servo]
      
      # The reason this works is complicated... but the algebra simplifies to this (strumming & fretting!)
      output((not new_state) and prev_state)

      shift(1) # Only shifting a single bit into one servo
    store()
    time.sleep_us(fret_max_angle - fret_min_angle)

    output(0)
    shift(num_servos) # Shifting 0 into ALL servos
    store()
    time.sleep_us(20_000 - fret_max_angle)

  # Return new "previous_states"
  return servo_states.copy()

if __name__ == "__main__":
    main_test()
