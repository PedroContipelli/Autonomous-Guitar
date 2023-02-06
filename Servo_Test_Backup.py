from machine import Pin
import time

led = Pin(2, Pin.OUT)
SER = Pin(0, Pin.OUT)
RCLK = Pin(4, Pin.OUT)
SRCLK = Pin(16, Pin.OUT)

def output(value):
  SER.value(value)

def shift(n):
  for i in range(n):
    SRCLK.value(1)
    SRCLK.value(0)

def store():
  RCLK.value(1)
  RCLK.value(0)

servo = [0] * 24
cycles = 10

def servo_write():
  for _ in range(cycles):
    min_angle = 100
    max_angle = 900
    
    output(1)
    shift(24)
    store()
    time.sleep_us(min_angle)
    
    for i in range(23,-1,-1):
      output(servo[i])
      shift(1)
    store()
    time.sleep_us(max_angle-min_angle)
    
    output(0)
    shift(24)
    store()
    time.sleep_us(20000-max_angle)

while True:
    for i in range (24):
      servo_write()
      time.sleep(0.55)
      servo[i] = 1
      servo_write()
      time.sleep(0.05)
      servo[i] = 0