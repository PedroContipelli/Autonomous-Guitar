int SER = 13;
int nOE = 12;
int RCLK = 11;
int SRCLK = 10;
int nSRCLR = 9;
int servo[8] = {0};

void setup() {
  pinMode(SER, OUTPUT);
  digitalWrite(SER, LOW);
  pinMode(nOE, OUTPUT);
  digitalWrite(nOE, LOW);
  pinMode(RCLK, OUTPUT);
  digitalWrite(RCLK, LOW);
  pinMode(SRCLK, OUTPUT);
  digitalWrite(SRCLK, LOW);
  pinMode(nSRCLR, OUTPUT);
  digitalWrite(nSRCLR, LOW);
  digitalWrite(nSRCLR, HIGH);
}

void output(int i) {
  digitalWrite(SER, i);
}

void shift(int i) {
  while (i-- > 0) {
    digitalWrite(SRCLK, HIGH);
    digitalWrite(SRCLK, LOW);
  }
}

void store() {
  digitalWrite(RCLK, HIGH);
  digitalWrite(RCLK, LOW);
}

void servoWrite() {
  const int low = 600;
  const int high = 2400;
  
  output(1);
  shift(8);
  store();
  delayMicroseconds(low);

  for (int i = 7; i >= 0; --i) {
    output(servo[i]);
    shift(1);
  }
  store();
  delayMicroseconds(high - low);

  output(0);
  shift(8);
  store();
  delayMicroseconds(20000 - high);
}

void loop() {
  servo[1] = 1;
  for (int i = 0; i < 200; ++i) {
    servoWrite();
  }
  servo[1] = 0;
  servo[2] = 1;
  for (int i = 0; i < 200; ++i) {
    servoWrite();
  }
  servo[1] = 1;
  for (int i = 0; i < 200; ++i) {
    servoWrite();
  }
  servo[1] = 0;
  servo[2] = 0;
  servo[3] = 1;
  for (int i = 0; i < 200; ++i) {
    servoWrite();
  }
  servo[1] = 1;
  for (int i = 0; i < 200; ++i) {
    servoWrite();
  }
  servo[1] = 0;
  servo[2] = 1;
  for (int i = 0; i < 200; ++i) {
    servoWrite();
  }
  servo[1] = 1;
  for (int i = 0; i < 200; ++i) {
    servoWrite();
  }
  servo[1] = 0;
  servo[2] = 0;
  servo[3] = 0;
  for (int i = 0; i < 200; ++i) {
    servoWrite();
  }
}
