#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ********************************************
# Serial message printer v1
# for feeding robot arm
# By Ye Liu
# Aug 9 2018
# ********************************************

import serial


class Printer(object):

    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(port, 9600)

    def print(self):
        print('* Listening on port:', self.port)
        while True:
            res = self.ser.readline()
            print('Receive:', res.decode(), end='')


if __name__ == '__main__':
    printer = Printer('/dev/cu.usbmodem14131')
    printer.print()
