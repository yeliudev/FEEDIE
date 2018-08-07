// ********************************************
// Serial Interaction Model v2
// for feeding robot arm
// By Ye Liu
// Aug 6 2018
// ********************************************

#include <Servo.h>

#define ROBOT_NAME "Friday"

#define ELBOW_MIN 0
#define ELBOW_MAX 60
#define ELBOW_DEFAULT 10

#define SHOULDER_MIN 0
#define SHOULDER_MAX 165
#define SHOULDER_DEFAULT 60

#define WRIST_X_MIN 30
#define WRIST_X_MAX 180
#define WRIST_X_DEFAULT 160

#define WRIST_Y_MIN 0
#define WRIST_Y_MAX 90
#define WRIST_Y_DEFAULT 90

#define WRIST_Z_MIN 0
#define WRIST_Z_MAX 180
#define WRIST_Z_DEFAULT 90

#define BASE_MIN 0
#define BASE_MAX 180
#define BASE_DEFAULT 100

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

int pos, speed, currentA, currentB, currentC, currentD, currentE, currentF, currentG;

String buffer = "";
int coordinate[2] = {0};
int flag = 0;

void servoReset()
{
  currentA = servoA.read();
  currentB = servoB.read();
  currentC = servoC.read();
  currentD = servoD.read();
  currentE = servoE.read();
  currentF = servoF.read();
  currentG = servoG.read();

  speed = 200;
  for (pos = 0; pos <= speed; pos++)
  {
    servoA.write(int(map(pos, 0, speed, currentA, ELBOW_DEFAULT)));
    servoB.write(int(map(pos, 0, speed, currentB, SHOULDER_DEFAULT)));
    servoC.write(int(map(pos, 0, speed, currentC, WRIST_X_DEFAULT)));
    servoD.write(int(map(pos, 0, speed, currentD, WRIST_Y_DEFAULT)));
    servoE.write(int(map(pos, 0, speed, currentE, WRIST_Z_DEFAULT)));
    servoF.write(int(map(pos, 0, speed, currentF, BASE_DEFAULT)));
    servoG.write(int(map(pos, 0, speed, currentG, CRAW_DEFAULT)));
    delay(5);
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
}

void loop()
{
  int j = 0;

  if (Serial.available() > 0)
  {
    buffer = Serial.readString();
    flag = 1;
  }

  if (flag == 1)
  {
    for (int i = 0; i < buffer.length(); i++)
    {
      if (buffer[i] == ',')
      {
        j++;
      }
      else
      {
        coordinate[j] = coordinate[j] * 10 + (buffer[i] - '0');
      }
    }

    buffer = String("");
    flag = 0;

    for (int i = 0; i < 2; i++)
    {
      Serial.println(coordinate[i]);
      coordinate[i] = 0;
    }
  }
