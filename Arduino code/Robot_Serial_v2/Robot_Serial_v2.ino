// ********************************************
// Serial Interaction Model v3
// for feeding robot arm
// By Ye Liu
// Aug 9 2018
// ********************************************

#include <Servo.h>

#define ELBOW_MIN 0
#define ELBOW_MAX 60
#define ELBOW_DEFAULT 5

#define SHOULDER_MIN 35
#define SHOULDER_MAX 120
#define SHOULDER_DEFAULT 95

#define WRIST_X_MIN 30
#define WRIST_X_MAX 180
#define WRIST_X_DEFAULT 120

#define WRIST_Y_MIN 0
#define WRIST_Y_MAX 90
#define WRIST_Y_DEFAULT 90

#define WRIST_Z_MIN 0
#define WRIST_Z_MAX 180
#define WRIST_Z_DEFAULT 85

#define BASE_MIN 0
#define BASE_MAX 180
#define BASE_DEFAULT 100
#define BASE_FACE 130
#define BASE_FOOD 170

#define CRAW_MIN 10 // open
#define CRAW_MAX 82 // close
#define CRAW_DEFAULT CRAW_MIN

#define CLIENT_MIDDLE_X 640
#define CLIENT_MIDDLE_Y 360

Servo servoA;
Servo servoB;
Servo servoC;
Servo servoD;
Servo servoE;
Servo servoF;
Servo servoG;

int pos, speed, currentA, currentB, currentC, currentD, currentE, currentF, currentG, len, comma, x, y;
String buffer;

void servoReset(int elbow = ELBOW_DEFAULT, int shoulder = SHOULDER_DEFAULT, int wristX = WRIST_X_DEFAULT, int wristY = WRIST_Y_DEFAULT, int wristZ = WRIST_Z_DEFAULT, int base = BASE_DEFAULT, int craw = CRAW_DEFAULT)
{
  currentA = servoA.read();
  currentB = servoB.read();
  currentC = servoC.read();
  currentD = servoD.read();
  currentE = servoE.read();
  currentF = servoF.read();
  currentG = servoG.read();

  speed = 100; // Lower is faster
  for (pos = 0; pos <= speed; pos++)
  {
    servoA.write(int(map(pos, 0, speed, currentA, elbow)));
    servoB.write(int(map(pos, 0, speed, currentB, shoulder)));
    servoC.write(int(map(pos, 0, speed, currentC, wristX)));
    servoD.write(int(map(pos, 0, speed, currentD, wristY)));
    servoE.write(int(map(pos, 0, speed, currentE, wristZ)));
    servoF.write(int(map(pos, 0, speed, currentF, base)));
    servoG.write(int(map(pos, 0, speed, currentG, craw)));
    delay(5);
  }
}

void refresh()
{
  buffer = "";
  len = 0;
}

void sayHello()
{
  servoC.write(180);
  for (int i = 85; i >= 35; i--)
  {
    servoE.write(i);
    delay(2);
  }
  for (int i = 35; i <= 135; i++)
  {
    servoE.write(i);
    delay(2);
  }
  for (int i = 135; i >= 35; i--)
  {
    servoE.write(i);
    delay(2);
  }
  for (int i = 35; i <= 135; i++)
  {
    servoE.write(i);
    delay(2);
  }
  for (int i = 135; i >= 85; i--)
  {
    servoE.write(i);
    delay(2);
  }
  servoC.write(120);
}

void trackObject(int x, int y)
{
  if (x > CLIENT_MIDDLE_X)
  {
    // Turn right
    int base = servoF.read();
    double delta = 180 / PI * atan((x - CLIENT_MIDDLE_X) / 1600.0);
    Serial.println("Turn " + String(delta) + "° right");
    servoF.write(base - delta);
  }
  else
  {
    // Turn left
    int base = servoF.read();
    double delta = 180 / PI * atan((CLIENT_MIDDLE_X - x) / 1600.0);
    Serial.println("Turn " + String(delta) + "° left");
    servoF.write(base + delta);
  }
  if (y > CLIENT_MIDDLE_Y)
  {
    // Turn up
    int elbow = servoA.read();
    double delta = 180 / PI * atan((y - CLIENT_MIDDLE_Y) / 1600.0);
    Serial.println("Turn " + String(delta) + "° up");
    servoA.write(elbow - delta);
  }
  else
  {
    // Turn down
    int elbow = servoA.read();
    double delta = 180 / PI * atan((CLIENT_MIDDLE_Y - y) / 1600.0);
    Serial.println("Turn " + String(delta) + "° down");
    servoA.write(elbow + delta);
  }
}

void setup()
{
  Serial.begin(9600);

  servoA.attach(2);
  servoB.attach(3);
  servoC.attach(4);
  servoD.attach(5);
  servoE.attach(6);
  servoF.attach(7);
  servoG.attach(8);

  servoReset();
  refresh();
  sayHello();
}

void loop()
{
  if (Serial.available() > 0)
  {
    // Read message from computer
    buffer = Serial.readStringUntil('q');
    len = buffer.length();
  }

  if (len)
  {
    /*
      Different char of buffer[0] represents for different command
      'c': coordinate
      'f': turn towards face
      'o': turn towards food
    */
    switch (buffer[0])
    {
    case 'c':
      // Parse coordinate data
      comma = buffer.indexOf(',');
      x = buffer.substring(1, comma).toInt();
      y = buffer.substring(comma + 1).toInt();

      // Track object
      trackObject(x, y);
    case 'f':
      servoReset();
      Serial.println("Turn to face");
    case '0':
      servoReset();
      Serial.println("Turn to food");
    }

    refresh();
  }
}
