#include <Wire.h> // I2C
#include <Adafruit_PWMServoDriver.h>

#define DEFAULT_I2C_ADDRESS 0x40
Adafruit_PWMServoDriver pca9685 = Adafruit_PWMServoDriver(DEFAULT_I2C_ADDRESS);

// Servo motor ports
#define SER0  0
#define SER1  1
#define SER2  2

void setup()
{
  Serial.begin(115200); // Sets baud rate (transmission bits per second)

  pca9685.begin();
  pca9685.setPWMFreq(50); // 50 Hz (period: 20,000 us)
}

void loop()
{
  print("MIN ANGLE 0");
  
  set_servo_angle(SER0, 0);
  set_servo_angle(SER1, 0);
  set_servo_angle(SER2, 0);

  delay(3000);

  print("MAX ANGLE 180");
  
  set_servo_angle(SER0, 180);
  set_servo_angle(SER1, 180);
  set_servo_angle(SER2, 180);

  delay(3000);
}

void set_servo_angle(int serial_port, int angle)
{
  for (int i = 0; i < 3; i++)
    pca9685.setPWM(serial_port, 0, to_ticks(angle));
}

// Servo pulse widths
#define MIN_ANGLE_TICKS  102  // 102 ticks / 4096 ticks = 500 us / 20,000 us
#define MAX_ANGLE_TICKS  512  // 512 ticks / 4096 ticks = 2500 us / 20,000 us

// Maps servo degree range (0 - 200) to tick range (102 - 512)
int to_ticks(int degrees)
{
  return map(degrees, 0, 200, MIN_ANGLE_TICKS, MAX_ANGLE_TICKS);
}

void print(String out)
{
  Serial.println(out);
}