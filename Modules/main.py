#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ********************************************
# Main programme v1
# for feeding robot arm
# By Ye Liu
# Aug 10 2018
# ********************************************

import threading
import time
from VoiceRecognizer import VoiceRecognizer
from ObjectRecognizer import ObjectRecognizer
from Printer import Printer

# Set serial port
port = '/dev/cu.usbmodem14131'

# Class instantiation
objectRecognizer = ObjectRecognizer(
    'ObjectRecognition', 0, port)
voiceRecognizer = VoiceRecognizer()
printer = Printer(port)

videoThread = threading.Thread(
    target=objectRecognizer.CatchUsbVideo, name='CatchUsbVideo')
videoThread.start()

time.sleep(5)
objectRecognizer.switchClassfier('bread')
