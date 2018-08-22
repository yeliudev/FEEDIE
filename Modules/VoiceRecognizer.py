#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ********************************************
# Voice Recognition Model v3
# for feeding robot arm
# By Ye Liu
# Aug 23 2018
# ********************************************

import wave
import pyaudio
import nltk
from time import sleep
from os import remove
from aip import AipSpeech
import numpy as np


class VoiceRecognizer(object):

    def __init__(self):
        self.APP_ID = '11615546'
        self.API_KEY = 'Agl9OnFc63ssaEXQGLvkop7c'
        self.SECRET_KEY = 'm206FgGobfv5jmdXTMnHtAY7kZ3gG8EH'

        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.RATE = 16000
        self.CHANNELS = 1
        self.RECORD_SECONDS = 1
        self.WAVE_OUTPUT_FILENAME = 'output.wav'

        self.NN_IGNORE_LIST = ['piece', 'cup',
                               'bottle', 'bar', 'spoon', 'bowl', 'oh']

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # Return keywords of the speech
    def recognize(self):
        # Recognize voice via Baidu API
        res = self.client.asr(self.get_file_content(self.WAVE_OUTPUT_FILENAME), 'wav', 16000, {
            'dev_pid': 1737,
        })

        # Remove temp wav file
        remove(self.WAVE_OUTPUT_FILENAME)

        if res['err_no'] == 0:
            print('Result:', res['result'][0])

            words = nltk.word_tokenize(str(res['result'][0]))
            tagged_words = nltk.pos_tag(words)
            # print('Tagged:', tagged_words)

            for item in tagged_words:
                if item[1] == 'NN' and item[0] in ['bread', 'breath', 'crap', 'crab']:
                    print('Keyword: bread\n')
                    return 'bread'

            for item in tagged_words:
                if item[1] == 'NN' and item[0] not in self.NN_IGNORE_LIST:
                    print('Keyword:', item[0], '\n')
                    return item[0]

            print('No keyword found\n')
            return False
        else:
            print('Error:', res['err_msg'], '\n')
            return False

    def monitor(self):
        print('* testing noise')
        sleep(1)

        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        while True:
            test_data = stream.read(self.CHUNK)
            noise_data = np.fromstring(test_data, dtype=np.short)
            noise = np.max(noise_data)
            if noise < 2000:
                print('noise:', noise, 'db\n')
                break
            else:
                print('too noisy')
                stream.stop_stream()
                sleep(1)
                stream.start_stream()

        stream.stop_stream()

        frames = []
        recording = False
        detecting = False
        index = -1

        while True:
            if not recording and not detecting:
                print('* detecting *')
                detecting = True
                stream.start_stream()

            for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                data = stream.read(self.CHUNK)
                frames.append(data)
                index += 1

            audio_data = np.fromstring(data, dtype=np.short)
            # large_sample_count = np.sum(audio_data > noise + 400)
            temp = np.max(audio_data)

            if temp > noise + 1000:
                if not recording:
                    print('* recording...')
                    record_index = index - 150
                    recording = True
                    detecting = False
                print('Signal detected:', temp, 'db')
            elif recording:
                print('* recognizing...')
                stream.stop_stream()
                recording = False
                rec = frames[record_index:]
                frames.clear()
                index = -1

                wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(rec))
                wf.close()

                self.recognize()


if __name__ == '__main__':
    detector = VoiceRecognizer()
    detector.monitor()
