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

fret_min_angle, fret_max_angle = (0, 50) # microseconds (fret lower <--> unfret higher)
strum_min_angle, strum_max_angle = (0, 500) # microseconds
cycle_duration = 10_000 # microseconds

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

  for cycle in range(cycles):
    stage1(stage_type="Fret")
    stage2(stage_type="Fret")
    stage3(stage_type="Fret")
    stage1(stage_type="Strum")
    stage2(stage_type="Strum")
    stage3(stage_type="Strum")

  # Becomes new "previous_states"
  return virtual_states.copy()

# Stage 1 controls whether servos are operating or completely OFF
def stage1(stage_type="Fret/Strum"):
    for virtual_servo in range(num_servos, 0, -1):
        prev_state, new_state = get_state(virtual_servo) # Accounts for physical mapping

        # Fretting servos only powered OFF when remaining in the up position
        if virtual_servo <= num_fret_servos:
            output(stage_type == "Fret" and (prev_state or new_state))
        # Strumming servos only powered ON whenever there's a change in state
        else:
            output(stage_type == "Strum" and (prev_state ^ new_state))

        shift() # Shift a single bit into one servo
    store() # Buffer release after loop has finished
    
    time.sleep_us(fret_min_angle if stage_type == "Fret" else strum_min_angle)
        
# Stage 2 controls serial data loading in
def stage2(stage_type="Fret/Strum"):
    for virtual_servo in range(num_servos, 0, -1):
        prev_state, new_state = get_state(virtual_servo) # Accounts for physical mapping

        # Still not 100% sure how this works lol
        if virtual_servo <= num_fret_servos:
            output(stage_type == "Fret" and ((not new_state) and prev_state))
        else:
            output(stage_type == "Strum" and ((not prev_state) and new_state))

        shift() # Shift a single bit into one servo
    store() # Buffer release after loop has finished

    if stage_type == "Strum":
        time.sleep_us(strum_max_angle - strum_min_angle)
    elif stage_type == "Fret":
        time.sleep_us(fret_max_angle - fret_min_angle)
        
def stage3(stage_type="Fret/Strum"):
    output(0)
    shift(num_servos) # Shifts 0 into ALL servos
    store() # Buffer release
    time.sleep_us(cycle_duration - (fret_max_angle if stage_type == "Fret" else strum_max_angle)) # Finish square wave?
    
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