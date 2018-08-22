#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ********************************************
# Main programme v2
# for feeding robot arm
# By Ye Liu
# Aug 10 2018
# ********************************************

import os

pid = os.fork()
if pid:
    os.execlp('python3', 'python3',
              '/Volumes/Data/Git/Feeding-Robot-Demo/Modules/ObjectRecognizer.py')
else:
    os.execlp('python3', 'python3',
              '/Volumes/Data/Git/Feeding-Robot-Demo/Modules/VoiceRecognizer.py')
