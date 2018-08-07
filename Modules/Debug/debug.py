#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial

ser = serial.Serial('/dev/cu.usbmodem14141', 9600)
ser.write(30)
line = ser.readline()
print(line.decode())
