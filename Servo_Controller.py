from machine import Pin
import time

led = Pin(2, Pin.OUT)
SER = Pin(0, Pin.OUT)
RCLK = Pin(4, Pin.OUT)
SRCLK = Pin(16, Pin.OUT)

cycles = 10

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
    max_angle = 900

    output(1)
    shift(num_servos)
    store()
    time.sleep_us(min_angle)

    for servo in range(num_servos, 0, -1):
      output(servo_states[servo])
      shift(1)

    store()
    time.sleep_us(max_angle - min_angle)

    output(0)
    shift(num_servos)
    store()
    time.sleep_us(20_000 - max_angle)
