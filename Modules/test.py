#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyautogui as pag
import time

time.sleep(3)
pag.keyDown('ctrlleft')
pag.keyDown('shiftleft')
pag.keyDown('q')

time.sleep(1)
pag.keyUp('ctrlleft')
pag.keyUp('shiftleft')
pag.keyUp('q')
