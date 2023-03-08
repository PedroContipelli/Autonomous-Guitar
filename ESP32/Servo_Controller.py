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

fret_min_angle, fret_max_angle = (120, 140) # (fret lower <--> unfret higher)
strum_min_angle, strum_max_angle = (0, 180)
cycle_duration = 10_000 # microseconds

# Values hardcoded for our specific servo model
def angle_to_microseconds(angle):
    return (angle/180) * 2000 + 500

def main_test():
    # mapping()
    # alignment()

    test_range_loop(min=26, max=26, reps=1, wait_time=1, cycles=10)

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
  global virtual_states, previous_states
  fret_outputs = precompute_stage_outputs(fret=True)
  strum_outputs = precompute_stage_outputs(strum=True)

  for cycle in range(cycles):
    a = time.time_ns()
    stage1(fret_outputs, fret=True)
    b = time.time_ns()
    stage2(fret_outputs, fret=True)
    c = time.time_ns()
    stage3(fret_outputs, fret=True)
    d = time.time_ns()

    stage1(strum_outputs, strum=True)
    e = time.time_ns()
    stage2(strum_outputs, strum=True)
    f = time.time_ns()
    stage3(strum_outputs, strum=True)
    g = time.time_ns()
    all = [x//1000 for x in (b-a, c-b, d-c, e-d, f-e, g-f)]
    print(all)

  # Becomes new "previous_states"
  return virtual_states.copy()

def precompute_stage_outputs(fret=False, strum=False):
    outputs = [(0,0) for _ in range(num_servos + 1)]

    for virtual_servo in range(num_servos, 0, -1):
        prev_state, new_state = get_state(virtual_servo) # Accounts for physical mapping

        if virtual_servo <= num_fret_servos:
            outputs[virtual_servo][0] = fret and (prev_state or new_state) # FRET STAGE 1
            outputs[virtual_servo][1] = fret and (not new_state) and prev_state) # FRET STAGE 2
        else:
            outputs[virtual_servo][0] = strum and (prev_state ^ new_state) # STRUM STAGE 1
            outputs[virtual_servo][1] = strum and (not new_state) and prev_state # STRUM STAGE 2

    return outputs

# 0 if servo is OFF | 1 if servo set to at least min_angle
def stage1(outputs, fret=False, strum=False):
    for virtual_servo in range(num_servos, 0, -1):
        output(outputs[virtual_servo][0])
        shift() # Shift a single bit into one servo
    store() # Buffer release after loop has finished

    sleep_time_us = angle_to_microseconds(fret_min_angle if fret else strum_min_angle)
    time.sleep_us(sleep_time_us)

# 0 if servo is OFF | 1 if servo is pushed further to max angle
def stage2(outputs, fret=False, strum=False):
    for virtual_servo in range(num_servos, 0, -1):
        output(outputs[virtual_servo][1])
        shift() # Shift a single bit into one servo
    store() # Buffer release after loop has finished

    sleep_time_us = 0
    if strum:
        sleep_time_us = angle_to_microseconds(strum_max_angle - strum_min_angle)
    elif fret:
        sleep_time_us = angle_to_microseconds(fret_max_angle - fret_min_angle)
    time.sleep_us(sleep_time_us)

# Always 0 (end square wave, complete duty cycle)
def stage3(fret=False, strum=False):
    output(0)
    shift(num_servos) # Shifts 0 into ALL servos
    store() # Buffer release
    time.sleep_us(cycle_duration - angle_to_microseconds(fret_max_angle if fret else strum_max_angle))

def get_state(virtual_servo):
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
