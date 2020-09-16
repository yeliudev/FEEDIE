# Copyright (c) Ye Liu. All rights reserved.

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
    printer = Printer('/dev/cu.usbmodem14141')
    printer.print()
