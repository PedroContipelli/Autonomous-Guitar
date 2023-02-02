from machine import Pin
import time

led = Pin(2, Pin.OUT)
SERIAL_OUT = Pin(0, Pin.OUT)
RCLK = Pin(4, Pin.OUT)
SRCLK = Pin(16, Pin.OUT)

def output(value):
  SERIAL_OUT.value(value)

def shift(n):
  for i in range(n):
    SRCLK.value(1)
    SRCLK.value(0)

def store():
  RCLK.value(1)
  RCLK.value(0)

cycles = 10

def servo_write(servo_state):
  for _ in range(cycles):
    min_angle = 100
    max_angle = 900

    output(1)
    shift(30)
    store()
    time.sleep_us(min_angle)

    num_servos = 30

    for i in range(num_servos):
      output(servo_state[num_servos - i - 1])
      shift(1)
    store()
    time.sleep_us(max_angle-min_angle)

    output(0)
    shift(num_servos)
    store()
    time.sleep_us(20000-max_angle)
