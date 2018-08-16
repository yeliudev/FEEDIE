#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ********************************************
# User Interface Model v2
# for feeding robot arm
# By Ye Liu
# Aug 15 2018
# ********************************************

import cv2
import nltk
import serial
import pyautogui as pag
from redis import StrictRedis
from flask import Flask, render_template, Response, request, jsonify

# run 'redis-server /usr/local/etc/redis.conf' first
ser = serial.Serial('/dev/cu.usbmodem14141', 9600)

# Redis initialization
redis = StrictRedis(host='localhost', port=6379, db=0)
redis.set('count', '0')
redis.set('classifier', '')


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(1)

        self.color = (0, 255, 0)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.faceClassifier = cv2.CascadeClassifier(
            '/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml')
        self.breadClassifier = cv2.CascadeClassifier(
            '/Volumes/Data/Git/Feeding-Robot-Demo/Classifier/cascade_bread_11stages.xml')
        self.breadClassifier2 = cv2.CascadeClassifier(
            '/Volumes/Data/Git/Feeding-Robot-Demo/Classifier/cascade_bread_6stages.xml')
        self.cupClassifier = cv2.CascadeClassifier(
            '/Volumes/Data/Git/Feeding-Robot-Demo/Classifier/cascade_cup_3stages.xml')
        self.cupClassifier2 = cv2.CascadeClassifier(
            '/Volumes/Data/Git/Feeding-Robot-Demo/Classifier/cascade_cup_8stages.xml')
        self.cupClassifier3 = cv2.CascadeClassifier(
            '/Volumes/Data/Git/Feeding-Robot-Demo/Classifier/cascade_cup_2stages.xml')
        self.cupClassifier4 = cv2.CascadeClassifier(
            '/Volumes/Data/Git/Feeding-Robot-Demo/Classifier/cascade_cup_3stages2.xml')
        self.classifier = self.faceClassifier

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ok, frame = self.video.read()
        if not ok:
            print('frame not found')
            return

        # Create gray level image
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Read command from redis
        command = redis.get('classifier')

        # Change classifier
        if command == b'bread':
            self.classifier = self.breadClassifier
        elif command == b'water':
            self.classifier = self.cupClassifier4
        else:
            self.classifier = self.faceClassifier

        # Object recognition
        if self.classifier:
            objectRects = self.classifier.detectMultiScale(
                grey, scaleFactor=1.1, minNeighbors=3, minSize=(150, 150))

            if len(objectRects):
                # Load the first object
                (x, y, w, h) = objectRects[0]
                center_x = int(x + w / 2)
                center_y = int(y + h / 2)

                if command == b'bread':
                    if center_x > 570 and center_x < 700:
                        count = int(redis.get('count'))
                        count += 1
                        if count >= 10:
                            # Send pick bread message
                            ser.write('p'.encode())
                            # Switch back to face classifier
                            redis.set('classifier', 'feed_food')
                            redis.set('count', '0')
                        else:
                            redis.set('count', str(count))
                    else:
                        redis.set('count', '0')
                elif command == b'water':
                    if center_x > 570 and center_x < 700:
                        count = int(redis.get('count'))
                        count += 1
                        if count >= 15:
                            # Send pick water message
                            ser.write('w'.encode())
                            # Switch back to face classifier
                            redis.set('classifier', 'feed_water')
                            redis.set('count', '0')
                        else:
                            redis.set('count', str(count))
                    else:
                        redis.set('count', '0')

                    # count = int(redis.get('count'))
                    # count += 1
                    # if count >= 15:
                    #     # Send pick water message
                    #     ser.write('w'.encode())
                    #     # Switch back to face classifier
                    #     redis.set('classifier', 'feed_water')
                    #     redis.set('count', '0')
                    # else:
                    #     redis.set('count', str(count))
                elif command == b'feed_food':
                    if center_x > 570 and center_x < 700:
                        count = int(redis.get('count'))
                        count += 1
                        if count >= 30:
                            # Send feed food message
                            ser.write('x'.encode())
                            # Switch back to face classifier
                            redis.set('classifier', '')
                            redis.set('count', '0')
                        else:
                            redis.set('count', str(count))
                    else:
                        redis.set('count', '0')
                elif command == b'feed_water':
                    if center_x > 570 and center_x < 700:
                        count = int(redis.get('count'))
                        count += 1
                        if count >= 30:
                            # Send feed water message
                            ser.write('s'.encode())
                            # Switch back to face classifier
                            redis.set('classifier', '')
                            redis.set('count', '0')
                        else:
                            redis.set('count', str(count))
                    else:
                        redis.set('count', '0')

                # Send serial data
                if command == b'water':
                    coordinate = 'z' + str(center_x) + \
                        ',' + str(center_y) + 'q'
                    ser.write(coordinate.encode())
                elif command != b'feed_food' and command != b'feed_water':
                    coordinate = 'c' + str(center_x) + \
                        ',' + str(center_y) + 'q'
                    ser.write(coordinate.encode())

                cv2.rectangle(frame, (x - 10, y - 10),
                              (x + w + 10, y + h + 10), self.color, 2)

                cv2.putText(frame, 'Size: %d%%' % int(
                    100 * h / frame.shape[0]), (x + 5, y + 30), self.font, 1, (255, 0, 255), 3)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/app_init')
def app_init():
    # Init classifier
    redis.set('status', '')
    # Init gesture
    ser.write('f'.encode())
    return 'Success'


@app.route('/status')
def status():
    return redis.get('classifier')


@app.route('/start_recording', methods=['GET'])
def start_recording():
    recording = redis.get('status')
    if not recording:
        # Start recording by pressing hotkey
        pag.hotkey('ctrlleft', 'shiftleft', 'q')
        redis.set('status', 'recording')
    return 'Success'


@app.route('/speech_recognition', methods=['GET'])
def speech_recognition():
    input = request.args.get('input')

    # Natural language processing
    words = nltk.word_tokenize(input)
    tagged_words = nltk.pos_tag(words)

    # Search for known keywords
    for item in tagged_words:
        if item[0] == 'Bread' or item[0] == 'bread':
            print('Keyword: bread\n')

            # Send 'object' message (turn towards desk)
            ser.write('o'.encode())

            # Switch classifier
            redis.set('classifier', 'bread')

            return jsonify({'keyword': 'Bread'})
        elif item[0] == 'Water' or item[0] == 'water':
            print('Keyword: water\n')

            # Send 'object' message
            ser.write('o'.encode())

            # Switch classifier
            redis.set('classifier', 'water')

            return jsonify({'keyword': 'Water'})
        elif item[0] == 'Hello' or item[0] == 'hello' or item[0] == 'Hi' or item[0] == 'hi' or item[0] == 'morning' or item[0] == 'afternoon' or item[0] == 'evening':
            # Send 'hello' message
            ser.write('h'.encode())

            return jsonify({'keyword': 'hello'})
        elif item[0] == 'Thank' or item[0] == 'thank' or item[0] == 'Thanks' or item[0] == 'thanks':
            print('Keyword: thank you\n')

            # Send 'thank you' message
            ser.write('t'.encode())

            return jsonify({'keyword': 'thank'})

    # Search for probable keywords
    for item in tagged_words:
        if item[1] == 'NN' and item[0] in ['Breath', 'breath', 'Crap', 'crap', 'Crab', 'crab', 'Brat', 'brat']:
            print('Keyword:', item[0], '(bread)\n')

            # Send 'object' message (turn towards desk)
            ser.write('o'.encode())

            # Switch classifier
            redis.set('classifier', 'bread')

            return jsonify({'keyword': 'bread?'})

        if item[1] == 'NN' and item[0] in ['What', 'what', 'Whatever', 'whatever', 'Walk', 'walk']:
            print('Keyword:', item[0], '(water)\n')

            # Send 'object' message (turn towards desk)
            ser.write('o'.encode())

            # Switch classifier
            redis.set('classifier', 'water')

            return jsonify({'keyword': 'water?'})

    # Search for other keywords
    for item in tagged_words:
        if item[1] == 'NN' and item[0] not in ['piece', 'cup',
                                               'bottle', 'bar', 'spoon', 'bowl', 'oh', 'please']:
            print('Keyword:', item[0], '\n')

            return jsonify({'keyword': item[0]})

    # No keyword found
    return jsonify({'keyword': ''})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
