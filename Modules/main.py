#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ********************************************
# Main programme v1
# for feeding robot arm
# By Ye Liu
# Aug 10 2018
# ********************************************

import os
from VoiceRecognizer import VoiceRecognizer
from ObjectRecognizer import ObjectRecognizer
from Printer import Printer

# Set serial port
port = '/dev/cu.usbmodem14131'

# printer = Printer(port)

pid = os.fork()
if pid:
    voiceRecognizer = VoiceRecognizer()
    voiceRecognizer.monitor()
else:
    objectRecognizer = ObjectRecognizer(
        'ObjectRecognition', 0, port)
    objectRecognizer.catchUsbVideo()
