// ********************************************
// Serial Interaction Model v4
// for feeding robot arm
// By Ye Liu
// Aug 15 2018
// ********************************************

#include <Servo.h>

#define ELBOW_MIN 0
#define ELBOW_MAX 60
#define ELBOW_DEFAULT 10

#define SHOULDER_MIN 35
#define SHOULDER_MAX 120
#define SHOULDER_DEFAULT 75

#define WRIST_X_MIN 30
#define WRIST_X_MAX 180
#define WRIST_X_DEFAULT 100

#define WRIST_Y_MIN 0
#define WRIST_Y_MAX 180
#define WRIST_Y_DEFAULT 100

#define WRIST_Z_MIN 0
#define WRIST_Z_MAX 180
#define WRIST_Z_DEFAULT 85

#define BASE_MIN 0
#define BASE_MAX 180
#define BASE_DEFAULT 100
#define BASE_FACE 130
#define BASE_FOOD 180

#define CRAW_OPEN 12
#define CRAW_CLOSE 82

#define CLIENT_MIDDLE_X 638
#define CLIENT_MIDDLE_Y 478

Servo servoA;
Servo servoB;
Servo servoC;
Servo servoD;
Servo servoE;
Servo servoF;
Servo servoG;

int pos, speed, currentA, currentB, currentC, currentD, currentE, currentF, currentG, len, comma, x, y;
String buffer;

void servoReset(int elbow = ELBOW_DEFAULT, int shoulder = SHOULDER_DEFAULT, int wristX = WRIST_X_DEFAULT, int wristY = WRIST_Y_DEFAULT, int wristZ = WRIST_Z_DEFAULT, int base = BASE_DEFAULT, int craw = CRAW_OPEN, int speed = 100)
{
  currentA = servoA.read();
  currentB = servoB.read();
  currentC = servoC.read();
  currentD = servoD.read();
  currentE = servoE.read();
  currentF = servoF.read();
  currentG = servoG.read();

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

void pickFood()
{
  speed = 200;

  currentA = servoA.read();
  currentB = servoB.read();
  currentC = servoC.read();
  currentD = servoD.read();
  currentE = servoE.read();
  currentG = servoG.read();

  for (pos = 0; pos <= speed; pos++)
  {
    servoA.write(int(map(pos, 0, speed, currentA, 105)));
    servoB.write(int(map(pos, 0, speed, currentB, 40)));
    servoC.write(int(map(pos, 0, speed, currentC, 170)));
    servoD.write(int(map(pos, 0, speed, currentD, WRIST_Y_DEFAULT)));
    servoE.write(int(map(pos, 0, speed, currentE, WRIST_Z_DEFAULT)));
    servoG.write(int(map(pos, 0, speed, currentG, CRAW_OPEN)));
    delay(5);
  }

  currentA = servoA.read();
  currentB = servoB.read();
  currentC = servoC.read();

  for (pos = 0; pos <= speed; pos++)
  {
    servoA.write(int(map(pos, 0, speed, currentA, 70)));
    servoB.write(int(map(pos, 0, speed, currentB, 35)));
    servoC.write(int(map(pos, 0, speed, currentC, 130)));
    delay(5);
  }

  delay(50);

  for (pos = 0; pos <= speed; pos++)
  {
    servoG.write(int(map(pos, 0, speed, CRAW_OPEN, CRAW_CLOSE)));
    delay(5);
  }

  delay(50);

  servoReset(ELBOW_DEFAULT, SHOULDER_DEFAULT, WRIST_X_DEFAULT, WRIST_Y_DEFAULT, WRIST_Z_DEFAULT, BASE_FACE, CRAW_CLOSE, 200);
}

void pickWater()
{
  speed = 200;

  currentA = servoA.read();
  currentB = servoB.read();
  currentC = servoC.read();
  currentD = servoD.read();
  currentE = servoE.read();
  currentG = servoG.read();

  for (pos = 0; pos <= speed; pos++)
  {
    servoA.write(int(map(pos, 0, speed, currentA, 85)));
    servoB.write(int(map(pos, 0, speed, currentB, 0)));
    servoC.write(int(map(pos, 0, speed, currentC, 180)));
    servoD.write(int(map(pos, 0, speed, currentD, WRIST_Y_DEFAULT)));
    servoE.write(int(map(pos, 0, speed, currentE, WRIST_Z_DEFAULT)));
    servoG.write(int(map(pos, 0, speed, currentG, CRAW_OPEN)));
    delay(5);
  }

  currentA = servoA.read();

  for (pos = 0; pos <= speed; pos++)
  {
    servoA.write(int(map(pos, 0, speed, currentA, 65)));
    delay(5);
  }

  delay(50);

  for (pos = 0; pos <= speed; pos++)
  {
    servoG.write(int(map(pos, 0, speed, CRAW_OPEN, CRAW_CLOSE)));
    delay(5);
  }

  delay(50);

  servoReset(ELBOW_DEFAULT, SHOULDER_DEFAULT, 105, WRIST_Y_DEFAULT, WRIST_Z_DEFAULT, BASE_FACE, 82, 300);

  currentD = servoD.read();
  currentE = servoE.read();

  for (pos = 0; pos <= speed; pos++)
  {
    servoD.write(int(map(pos, 0, speed, currentD, 20)));
    servoE.write(int(map(pos, 0, speed, currentE, 170)));
    delay(5);
  }

  currentC = servoC.read();

  for (pos = 0; pos <= speed; pos++)
  {
    servoC.write(int(map(pos, 0, speed, currentC, 55)));
    delay(5);
  }
}

void feedFood()
{
  delay(1000);

  speed = 200;

  for (pos = 0; pos <= speed; pos++)
  {
    servoG.write(int(map(pos, 0, speed, CRAW_CLOSE, CRAW_OPEN)));
    delay(5);
  }
}

void feedWater()
{
  speed = 200;

  delay(1000);

  currentD = servoD.read();

  for (pos = 0; pos <= 1200; pos++)
  {
    servoD.write(int(map(pos, 0, speed, currentD, 130)));
    delay(5);
  }

  delay(3000);

  currentD = servoD.read();

  for (pos = 0; pos <= 200; pos++)
  {
    servoD.write(int(map(pos, 0, speed, currentD, 20)));
    delay(5);
  }

  delay(5);

  servoReset(65, 0, 180, WRIST_Y_DEFAULT, WRIST_Z_DEFAULT, BASE_FOOD, CRAW_CLOSE, 200);

  delay(500);

  for (pos = 0; pos <= speed; pos++)
  {
    servoG.write(int(map(pos, 0, speed, CRAW_CLOSE, CRAW_OPEN)));
    delay(5);
  }

  delay(50);

  for (pos = 0; pos <= speed; pos++)
  {
    servoA.write(int(map(pos, 0, speed, 65, 85)));
    delay(5);
  }

  delay(50);

  servoReset(ELBOW_DEFAULT, SHOULDER_DEFAULT, WRIST_X_DEFAULT, WRIST_Y_DEFAULT, WRIST_Z_DEFAULT, BASE_FACE, CRAW_OPEN, 150);
}

void refresh()
{
  buffer = "";
  len = 0;
}

void sayHello()
{
  servoReset(ELBOW_DEFAULT, SHOULDER_DEFAULT, WRIST_X_MAX, WRIST_Y_DEFAULT, WRIST_Z_DEFAULT, BASE_FACE, CRAW_OPEN, 100);
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
  servoC.write(WRIST_X_DEFAULT);
}

void youAreWelcome()
{
  servoReset(ELBOW_DEFAULT, SHOULDER_DEFAULT, WRIST_X_MAX, WRIST_Y_DEFAULT, WRIST_Z_DEFAULT, BASE_FACE, CRAW_OPEN, 100);
  for (int i = WRIST_X_MAX; i >= 40; i--)
  {
    servoC.write(i);
    delay(2);
  }
  for (int i = 40; i <= 160; i++)
  {
    servoC.write(i);
    delay(2);
  }
  for (int i = WRIST_X_MAX; i >= 40; i--)
  {
    servoC.write(i);
    delay(2);
  }
  servoC.write(WRIST_X_DEFAULT);
}

void trackObject(int x, int y)
{
  if (x < CLIENT_MIDDLE_X)
  {
    // Turn left
    int base = servoF.read();
    double delta = 180 / PI * atan((CLIENT_MIDDLE_X - x) / 4000.0);
    Serial.println("Turn " + String(delta) + "° left");
    servoF.write(base + delta);
  }
  else
  {
    // Turn right
    int base = servoF.read();
    double delta = 180 / PI * atan((x - CLIENT_MIDDLE_X) / 4000.0);
    Serial.println("Turn " + String(delta) + "° right");
    servoF.write(base - delta);
  }
  if (y < CLIENT_MIDDLE_Y)
  {
    // Turn up
    int elbow = servoA.read();
    double delta = 180 / PI * atan((CLIENT_MIDDLE_Y - y) / 8000.0);
    Serial.println("Turn " + String(delta) + "° up");
    servoA.write(elbow - delta);
  }
  else
  {
    // Turn down
    int elbow = servoA.read();
    double delta = 180 / PI * atan((y - CLIENT_MIDDLE_Y) / 8000.0);
    Serial.println("Turn " + String(delta) + "° down");
    servoA.write(elbow + delta);
  }
}

void trackObjectBalance(int x, int y)
{
  if (x < CLIENT_MIDDLE_X)
  {
    // Turn left
    int base = servoF.read();
    int head = servoC.read();
    double delta = 180 / PI * atan((CLIENT_MIDDLE_X - x) / 4000.0);
    Serial.println("Turn " + String(delta) + "° left");
    servoF.write(base + delta);
    servoC.write(head + delta);
  }
  else
  {
    // Turn right
    int base = servoF.read();
    int head = servoC.read();
    double delta = 180 / PI * atan((x - CLIENT_MIDDLE_X) / 4000.0);
    Serial.println("Turn " + String(delta) + "° right");
    servoF.write(base - delta);
    servoC.write(head - delta);
  }
  if (y < CLIENT_MIDDLE_Y)
  {
    // Turn up
    int elbow = servoA.read();
    int wrist = servoD.read();
    double delta = 180 / PI * atan((CLIENT_MIDDLE_Y - y) / 8000.0);
    if (elbow - delta > 0 && wrist + delta < 180)
    {
      Serial.println("Turn " + String(delta) + "° up");
      servoA.write(elbow - delta);
      servoD.write(wrist + delta);
    }
  }
  else
  {
    // Turn down
    int elbow = servoA.read();
    int wrist = servoD.read();
    double delta = 180 / PI * atan((y - CLIENT_MIDDLE_Y) / 8000.0);
    if (wrist - delta > 0)
    {
      Serial.println("Turn " + String(delta) + "° down");
      servoA.write(elbow + delta);
      servoD.write(wrist - delta);
    }
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
      'z': coordinate (carrying water)
      'f': turn towards face
      'o': turn towards desk
      'p': pick food
      'w': pick water
      'x': feed food
      's': feed water
      'h': say hello
      't': you are welcome
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
      break;
    case 'z':
      // Parse coordinate data
      comma = buffer.indexOf(',');
      x = buffer.substring(1, comma).toInt();
      y = buffer.substring(comma + 1).toInt();
      // Track object
      trackObjectBalance(x, y);
      break;
    case 'f':
      servoReset(ELBOW_DEFAULT, SHOULDER_DEFAULT, WRIST_X_DEFAULT, WRIST_Y_DEFAULT, WRIST_Z_DEFAULT, BASE_FACE, CRAW_OPEN, 100);
      Serial.println("Turn towards face");
      break;
    case 'o':
      servoReset(65, SHOULDER_DEFAULT, 110, WRIST_Y_DEFAULT, WRIST_Z_DEFAULT, BASE_FOOD, CRAW_OPEN, 150);
      Serial.println("Turn towards desk");
      break;
    case 'p':
      pickFood();
      Serial.println("Pick food");
      break;
    case 'w':
      pickWater();
      Serial.println("Pick water");
      break;
    case 'x':
      feedFood();
      Serial.println("Feed food");
      break;
    case 's':
      feedWater();
      Serial.println("Feed water");
      break;
    case 'h':
      sayHello();
      Serial.println("Say hello");
      break;
    case 't':
      youAreWelcome();
      Serial.println("You are welcome");
      break;
    }
    refresh();
  }
}
