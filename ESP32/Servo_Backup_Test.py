from machine import Pin
import time

led = Pin(2, Pin.OUT)
SER = Pin(0, Pin.OUT)
RCLK = Pin(4, Pin.OUT)
SRCLK = Pin(16, Pin.OUT)

# DOES NOT ACCOUNT FOR PHYSICAL MAPPING
num_servos = 30
servo_states = [0 for _ in range(num_servos)]
cycles = 10
wait_time = 0.20

def main():
    servo_write()
    time.sleep(wait_time)

    for servo in range(num_servos):
      print(f"Servo #{servo} ON\n")
      servo_states[servo] = 1
      servo_write()
      time.sleep(wait_time)

      print(f"Servo #{servo} OFF\n")
      servo_states[servo] = 0
      servo_write()
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

def servo_write():
  for _ in range(cycles):
    min_angle = 100
    max_angle = 500

    output(1)
    shift(num_servos)
    store()
    time.sleep_us(min_angle)

    for servo in range(num_servos, 0, -1):
      output(1 - servo_states[servo])
      shift(1)

    store()
    time.sleep_us(max_angle - min_angle)

    output(0)
    shift(num_servos)
    store()
    time.sleep_us(20_000 - max_angle)

if __name__ == "__main__":
    main()
