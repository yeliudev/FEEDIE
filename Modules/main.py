# Copyright (c) Ye Liu. All rights reserved.

import os

pid = os.fork()
if pid:
    os.execlp('python3', 'python3', 'Modules/ObjectRecognizer.py')
else:
    os.execlp('python3', 'python3', 'Modules/VoiceRecognizer.py')
