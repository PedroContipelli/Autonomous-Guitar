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
num_fret_servos = 24

fret_min_angle, fret_max_angle = (55, 170) # (fret lower <--> unfret higher)
strum_min_angle, strum_max_angle = (120, 180)

# Values hardcoded for our specific servo model
def angle_to_us(angle):
    return int((angle/180) * 2000 + 500)

fret_min_us, fret_max_us = (angle_to_us(fret_min_angle), angle_to_us(fret_max_angle))
strum_min_us, strum_max_us = (angle_to_us(strum_min_angle), angle_to_us(strum_max_angle))

def main_test():
    # mapping()
    alignment()

    # test_range_loop(min=26, max=26, reps=1, wait_time=1, cycles=30)

def alignment(at_a_time=3):
    global virtual_states, previous_states
    virtual_states = [0 for _ in range(num_servos + 1)]
    previous_states = virtual_states.copy()

    for servo in range(1, num_servos, at_a_time):
        print(f"Aligning Servos #{servo} - {servo + at_a_time - 1}")
        for s in range(servo, servo + at_a_time):
            previous_states[s] = 1
        previous_states = servo_write(cycles=20)
        time.sleep(0.15)
    time.sleep(2)

def mapping():
    test_range_loop(reps=3, wait_time=1, cycles=10)

# Counts up powering each servo ON and OFF once
def test_range_loop(min=1, max=30, reps=1, wait_time=0.5, cycles=15):
    global virtual_states, previous_states
    while True:
        virtual_states = [0 for _ in range(num_servos + 1)]
        previous_states = virtual_states.copy()

        for servo in range(min, max + 1):
          for _ in range(reps):
              print(f"Servo #{servo} ON\n")
              virtual_states[servo] = 1
              previous_states = servo_write(cycles=cycles)

              print(f"Servo #{servo} OFF\n")
              virtual_states[servo] = 0
              previous_states = servo_write(cycles=cycles)
              time.sleep(wait_time)

# Note: Servo states are 1-indexed (by physical convention)
def servo_write(cycles=15):
  global virtual_states, previous_states, outputs
  outputs = precompute_stage_outputs()
  delays = (0, fret_min_us, fret_max_us, 10_000, 10_000+strum_min_us, 10_000+strum_max_us, 19_400)
  time_left = [0 for _ in range(7)]

  for cycle in range(cycles):
      start_time = -1
      
      for stage, delay in enumerate(delays):
          # Shift
          for virtual_servo in range(num_servos, 0, -1):
              SER.value(outputs[virtual_servo][stage]) # Serial data
              SRCLK.value(1) # shift 1 bit
              SRCLK.value(0) # ^^^^^
              
          # Delay
          elapsed = time.ticks_us() - start_time
          time_left[stage] = delay - elapsed
          time.sleep_us(max(0, time_left[stage]))
          
          # Output (release buffer of all 30 bits)
          RCLK.value(1)
          RCLK.value(0)
          
          if start_time == -1:
              start_time = time.ticks_us()

  print(time_left)

  # Becomes new "previous_states"
  return virtual_states.copy()

def precompute_stage_outputs():
    outputs = [[0,0,0,0,0,0,0] for _ in range(num_servos + 1)]

    for virtual_servo in range(num_servos, 0, -1):
        prev_state, new_state = get_state(virtual_servo) # Accounts for physical mapping

        if virtual_servo <= num_fret_servos:
            outputs[virtual_servo][0] = prev_state or new_state # FRET STAGE 1 (min angle)
            outputs[virtual_servo][1] = (not new_state) and prev_state # FRET STAGE 2 (max angle)
        else:
            outputs[virtual_servo][3] = prev_state ^ new_state # STRUM STAGE 1 (min angle)
            outputs[virtual_servo][4] = (not new_state) and prev_state # STRUM STAGE 2 (max angle)

    return outputs

def get_state(virtual_servo):
    global previous_states, virtual_states
    true_servo = physical_map[virtual_servo] # Adapts to physical wiring changes
    return (previous_states[true_servo], virtual_states[true_servo])

def output(value):
    SER.value(value)

def shift(n=1):
  for i in range(n):
    SRCLK.value(1)
    SRCLK.value(0)

def store():
  RCLK.value(1)
  RCLK.value(0)

if __name__ == "__main__":
    main_test()
