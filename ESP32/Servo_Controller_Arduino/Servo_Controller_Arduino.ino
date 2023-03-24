#include <Wire.h> // I2C
#include <Adafruit_PWMServoDriver.h>
// SPLIT CODE INTO INDIVIDUAL FILES EVENTUALLY

// Servo Shield is PCA9685
Adafruit_PWMServoDriver driver1 = Adafruit_PWMServoDriver(0x40); // 0x40 = DEFAULT I2C BASE ADDRESS
Adafruit_PWMServoDriver driver2 = Adafruit_PWMServoDriver(0x41); // 2nd shield soldered to 1 offset

// Servo #s are 1-indexed. Port #s are 0-indexed.
// --------------- 1, 2, 3, 4, 5, 6,  7,  8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
int myServos[] = { 5, 1, 4, 6, 3, 2, 12, 10, 9,  7,  8, 11, 17, 13, 14, 16, 18, 15, 21, 22, 23, 24, 19, 20, 27, 26, 29, 28, 30, 25};

#define FRET_DOWN 110
#define FRET_UP 190

#define STRUM_DOWN 130
#define STRUM_UP 180


void setup()
{
  Serial.begin(115200); // Sets baud rate (transmission bits per second)

  driver1.begin();
  driver1.setPWMFreq(50); // 50 Hz (period: 20,000 us)

  driver2.begin();
  driver2.setPWMFreq(50); // 50 Hz (period: 20,000 us)

  delay(1000);

  // START CONTROL

  // FRETS
  for (int servo_num = 1; servo_num <= 24; servo_num++)
  {
    print("Powering servo" + String(servo_num));
    set_servo_angle(servo_num, FRET_DOWN);
    delay(700);
    set_servo_angle(servo_num, FRET_UP);
    delay(700);
    idle(servo_num);
    delay(500);
  }

  // STRUMS
  for (int servo_num = 25; servo_num <= 30; servo_num++)
  {
    print("Powering servo" + String(servo_num));
    set_servo_angle(servo_num, STRUM_DOWN);
    delay(700);
    set_servo_angle(servo_num, STRUM_UP);
    delay(700);
    idle(servo_num);
    delay(500);
  }


}


void loop()
{

}

void set_servo_angle(int servo_num, int angle)
{
  int serial_port = get_port(servo_num);
  int angle_ticks = (angle == -1) ? 4096 : to_ticks(angle);

  for (int i = 0; i < 3; i++)
  {
    if (0 <= serial_port && serial_port <= 15)
      driver1.setPWM(serial_port, 0, angle_ticks);

    else if (16 <= serial_port && serial_port <= 29)
      driver2.setPWM(serial_port - 16, 0, angle_ticks);
      
    else
      print("Error");
  }
}

void idle(int servo_num)
{
  set_servo_angle(servo_num, -1);
}

// Servo full pulse range widths
#define MIN_ANGLE_TICKS  102  // 102 ticks / 4095 ticks = 500 us / 20,000 us
#define MAX_ANGLE_TICKS  512  // 512 ticks / 4095 ticks = 2500 us / 20,000 us

// Maps servo degree range (0 - 200) to tick range (102 - 512)
int to_ticks(int degrees)
{
  return map(degrees, 0, 200, MIN_ANGLE_TICKS, MAX_ANGLE_TICKS);
}

void print(String out)
{
  Serial.println(out);
}

int get_port(int servo_num)
{
  for (int port = 0; port < 30; port++)
    if (myServos[port] == servo_num)
      return port;
  
  return -1;
}