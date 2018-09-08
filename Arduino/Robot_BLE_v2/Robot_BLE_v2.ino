// ********************************************
// Bluetooth Interaction Model v2
// for feeding robot arm
// By Ye Liu
// Originate from Dr. Benny Lo
// Aug 2 2018
// ********************************************

#include <CurieBLE.h>
#include <Servo.h>

#define ROBOT_NAME "Friday"

#define ELBOW_MIN 0
#define ELBOW_MAX 140
#define ELBOW_DEFAULT 60

#define SHOULDER_MIN 0
#define SHOULDER_MAX 165
#define SHOULDER_DEFAULT 100

#define WRIST_X_MIN 0
#define WRIST_X_MAX 180
#define WRIST_X_DEFAULT 80

#define WRIST_Y_MIN 0
#define WRIST_Y_MAX 90
#define WRIST_Y_DEFAULT 90

#define WRIST_Z_MIN 0
#define WRIST_Z_MAX 180
#define WRIST_Z_DEFAULT 66

#define BASE_MIN 0
#define BASE_MAX 180
#define BASE_DEFAULT 90

#define CRAW_MIN 10 // open
#define CRAW_MAX 82 // close
#define CRAW_DEFAULT CRAW_MIN

Servo servoA;
Servo servoB;
Servo servoC;
Servo servoD;
Servo servoE;
Servo servoF;
Servo servoG;

int pos, speed, sea, seb, sec, sed, see, sef, seg;

BLEPeripheral blePeripheral;
BLEService BrobotService("47452000-0f63-5b27-9122-728099603712");

BLECharCharacteristic BLE_ServoA("47452001-0f63-5b27-9122-728099603712", BLERead | BLEWrite);
BLECharCharacteristic BLE_ServoB("47452002-0f63-5b27-9122-728099603712", BLERead | BLEWrite);
BLECharCharacteristic BLE_ServoC("47452003-0f63-5b27-9122-728099603712", BLERead | BLEWrite);
BLECharCharacteristic BLE_ServoD("47452004-0f63-5b27-9122-728099603712", BLERead | BLEWrite);
BLECharCharacteristic BLE_ServoE("47452005-0f63-5b27-9122-728099603712", BLERead | BLEWrite);
BLECharCharacteristic BLE_ServoF("47452006-0f63-5b27-9122-728099603712", BLERead | BLEWrite);
BLECharCharacteristic BLE_ServoG("47452008-0f63-5b27-9122-728099603712", BLERead | BLEWrite);
BLECharCharacteristic BLE_Reset("47452007-0f63-5b27-9122-728099603712", BLEWrite);

void servoReset()
{
  sea = servoA.read();
  seb = servoB.read();
  sec = servoC.read();
  sed = servoD.read();
  see = servoE.read();
  sef = servoF.read();
  seg = servoG.read();

  speed = 500;
  for (pos = 0; pos <= speed; pos++)
  {
    servoA.write(int(map(pos, 1, speed, sea, ELBOW_DEFAULT)));
    servoB.write(int(map(pos, 1, speed, seb, SHOULDER_DEFAULT)));
    servoC.write(int(map(pos, 1, speed, sec, WRIST_X_DEFAULT)));
    servoD.write(int(map(pos, 1, speed, sed, WRIST_Y_DEFAULT)));
    servoE.write(int(map(pos, 1, speed, see, WRIST_Z_DEFAULT)));
    servoF.write(int(map(pos, 1, speed, sef, BASE_DEFAULT)));
    servoG.write(int(map(pos, 1, speed, seg, CRAW_DEFAULT)));
    delay(5);
  }
}

void blePeripheralConnectHandler(BLECentral &central)
{
  Serial.print("Connected event, central: ");
  Serial.println(central.address());
}

void blePeripheralDisconnectHandler(BLECentral &central)
{
  Serial.print("Disconnected event, central: ");
  Serial.println(central.address());
  servoReset();
}

void ServoACharacteristicWritten(BLECentral &central, BLECharacteristic &characteristic)
{
  Serial.print("ServoA Control: ");
  servoA.write((byte)BLE_ServoA.value());
  Serial.println((byte)BLE_ServoA.value(), DEC);
}

void ServoBCharacteristicWritten(BLECentral &central, BLECharacteristic &characteristic)
{
  Serial.print("ServoB Control: ");
  servoB.write((byte)BLE_ServoB.value());
  Serial.println((byte)BLE_ServoB.value(), DEC);
}
void ServoCCharacteristicWritten(BLECentral &central, BLECharacteristic &characteristic)
{
  Serial.print("ServoC Control: ");
  servoC.write((byte)BLE_ServoC.value());
  Serial.println((byte)BLE_ServoC.value(), DEC);
}
void ServoDCharacteristicWritten(BLECentral &central, BLECharacteristic &characteristic)
{
  Serial.print("ServoD Control: ");
  servoD.write((byte)BLE_ServoD.value());
  Serial.println((byte)BLE_ServoD.value(), DEC);
}

void ServoECharacteristicWritten(BLECentral &central, BLECharacteristic &characteristic)
{
  Serial.print("ServoE Control: ");
  servoE.write((byte)BLE_ServoE.value());
  Serial.println((byte)BLE_ServoE.value(), DEC);
}

void ServoFCharacteristicWritten(BLECentral &central, BLECharacteristic &characteristic)
{
  Serial.print("ServoF Control: ");
  servoF.write((byte)BLE_ServoF.value());
  Serial.println((byte)BLE_ServoF.value(), DEC);
}

void ServoGCharacteristicWritten(BLECentral &central, BLECharacteristic &characteristic)
{
  Serial.print("ServoG Control: ");
  servoG.write((byte)BLE_ServoG.value());
  Serial.println((byte)BLE_ServoG.value(), DEC);
}

void ResetCharacteristicWritten(BLECentral &central, BLECharacteristic &characteristic)
{
  Serial.println("Reset");
  servoReset();
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

  servoA.write(ELBOW_DEFAULT);
  servoB.write(SHOULDER_DEFAULT);
  servoC.write(WRIST_X_DEFAULT);
  servoD.write(WRIST_Y_DEFAULT);
  servoE.write(WRIST_Z_DEFAULT);
  servoF.write(BASE_DEFAULT);
  servoG.write(CRAW_DEFAULT);

  blePeripheral.setLocalName(ROBOT_NAME);
  blePeripheral.setAdvertisedServiceUuid(BrobotService.uuid());

  // Add service and characteristic
  blePeripheral.addAttribute(BrobotService);
  blePeripheral.addAttribute(BLE_ServoA);
  blePeripheral.addAttribute(BLE_ServoB);
  blePeripheral.addAttribute(BLE_ServoC);
  blePeripheral.addAttribute(BLE_ServoD);
  blePeripheral.addAttribute(BLE_ServoE);
  blePeripheral.addAttribute(BLE_ServoF);
  blePeripheral.addAttribute(BLE_ServoG);
  blePeripheral.addAttribute(BLE_Reset);

  // Assign event handlers for connected, disconnected to peripheral
  blePeripheral.setEventHandler(BLEConnected, blePeripheralConnectHandler);
  blePeripheral.setEventHandler(BLEDisconnected, blePeripheralDisconnectHandler);

  // Assign event handlers for characteristic
  BLE_ServoA.setEventHandler(BLEWritten, ServoACharacteristicWritten);
  BLE_ServoB.setEventHandler(BLEWritten, ServoBCharacteristicWritten);
  BLE_ServoC.setEventHandler(BLEWritten, ServoCCharacteristicWritten);
  BLE_ServoD.setEventHandler(BLEWritten, ServoDCharacteristicWritten);
  BLE_ServoE.setEventHandler(BLEWritten, ServoECharacteristicWritten);
  BLE_ServoF.setEventHandler(BLEWritten, ServoFCharacteristicWritten);
  BLE_ServoG.setEventHandler(BLEWritten, ServoGCharacteristicWritten);
  BLE_Reset.setEventHandler(BLEWritten, ResetCharacteristicWritten);

  // Set an initial value for the characteristic
  BLE_ServoA.setValue(ELBOW_DEFAULT);
  BLE_ServoB.setValue(SHOULDER_DEFAULT);
  BLE_ServoC.setValue(WRIST_X_DEFAULT);
  BLE_ServoD.setValue(WRIST_Y_DEFAULT);
  BLE_ServoE.setValue(WRIST_Z_DEFAULT);
  BLE_ServoF.setValue(BASE_DEFAULT);
  BLE_ServoG.setValue(CRAW_DEFAULT);

  // Advertise the service
  blePeripheral.begin();
  blePeripheral.poll();
  servoReset();

  Serial.println("Bluetooth device active, waiting for connections...");
}

void loop() {}
