# Copyright (c) Ye Liu. All rights reserved.

import cv2
import nltk
import pyautogui as pag
import serial
from flask import Flask, Response, jsonify, render_template, request
from redis import StrictRedis

# run 'redis-server /usr/local/etc/redis.conf'
# and set hotkey of 'Dictation' to 'ctrl + shift + q' first
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
            '/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml'  # noqa
        )
        self.breadClassifier = cv2.CascadeClassifier(
            'Classifier/cascade_bread_18-8-13_11stages.xml')
        self.cupClassifier = cv2.CascadeClassifier(
            'Classifier/cascade_cup_18-8-16_6stages.xml')
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
            self.classifier = self.cupClassifier
        else:
            self.classifier = self.faceClassifier

        # Object recognition
        if self.classifier:
            objectRects = self.classifier.detectMultiScale(
                grey, scaleFactor=1.1, minNeighbors=3, minSize=(150, 150))

            if len(objectRects):
                # Load the biggest object
                size = 0
                for rect in objectRects:
                    if rect[2] * rect[3] > size:
                        (x, y, w, h) = rect

                # Get center point coordinate
                center_x = int(x + w / 2)
                center_y = int(y + h / 2)

                # Show detected object
                cv2.rectangle(frame, (x - 10, y - 10),
                              (x + w + 10, y + h + 10), self.color, 2)

                cv2.putText(frame,
                            'Size: %d%%' % int(100 * h / frame.shape[0]),
                            (x + 5, y + 30), self.font, 1, (255, 0, 255), 3)

                # Position detection
                if command in [b'bread', b'water']:
                    if center_x > 570 and center_x < 700:
                        count = int(redis.get('count')) + 1
                        if count >= 10:
                            # Send 'pick' message and switch classifier
                            if command == b'bread':
                                ser.write('p'.encode())
                                redis.set('classifier', 'feed_food')
                            else:
                                ser.write('w'.encode())
                                redis.set('classifier', 'feed_water')

                            # Reset count
                            redis.set('count', '0')

                            # Return real-time image
                            ret, jpeg = cv2.imencode('.jpg', frame)
                            return jpeg.tobytes()
                        else:
                            redis.set('count', str(count))
                    else:
                        redis.set('count', '0')
                elif command in [b'feed_food', b'feed_water']:
                    if center_x > 570 and center_x < 700:
                        count = int(redis.get('count')) + 1
                        if count >= 15:
                            # Send 'feed' message
                            if command == b'feed_food':
                                ser.write('x'.encode())
                            else:
                                ser.write('s'.encode())

                            # Switch back to face classifier
                            redis.set('classifier', '')
                            redis.set('count', '0')

                            # Return real-time image
                            ret, jpeg = cv2.imencode('.jpg', frame)
                            return jpeg.tobytes()
                        else:
                            redis.set('count', str(count))
                    else:
                        redis.set('count', '0')

                # Send serial data
                if command == b'water':
                    coordinate = 'z' + str(center_x) + \
                        ',' + str(center_y) + 'q'
                    ser.write(coordinate.encode())
                else:
                    coordinate = 'c' + str(center_x) + \
                        ',' + str(center_y) + 'q'
                    ser.write(coordinate.encode())

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
    return Response(
        gen(VideoCamera()),
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

            # Send 'object' message (turn towards table)
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
        elif item[0] == 'Hello' or item[0] == 'hello' or item[
                0] == 'Hi' or item[0] == 'hi' or item[0] == 'morning' or item[
                    0] == 'afternoon' or item[0] == 'evening':
            # Send 'hello' message
            ser.write('h'.encode())

            return jsonify({'keyword': 'hello'})
        elif item[0] == 'Thank' or item[0] == 'thank' or item[
                0] == 'Thanks' or item[0] == 'thanks':
            print('Keyword: thank you\n')

            # Send 'thank you' message
            ser.write('t'.encode())

            return jsonify({'keyword': 'thank'})

    # Search for probable keywords
    for item in tagged_words:
        if item[1] == 'NN' and item[0] in [
                'Breath', 'breath', 'Crap', 'crap', 'Crab', 'crab', 'Brat',
                'brat'
        ]:
            print('Keyword:', item[0], '(bread)\n')

            # Send 'object' message (turn towards table)
            ser.write('o'.encode())

            # Switch classifier
            redis.set('classifier', 'bread')

            return jsonify({'keyword': 'bread?'})

        if item[1] == 'NN' and item[0] in [
                'What', 'what', 'Whatever', 'whatever', 'Walk', 'walk'
        ]:
            print('Keyword:', item[0], '(water)\n')

            # Send 'object' message (turn towards table)
            ser.write('o'.encode())

            # Switch classifier
            redis.set('classifier', 'water')

            return jsonify({'keyword': 'water?'})

    # Search for other keywords
    for item in tagged_words:
        if item[1] == 'NN' and item[0] not in [
                'piece', 'cup', 'tea', 'bottle', 'bar', 'spoon', 'bowl', 'oh',
                'please'
        ]:
            print('Keyword:', item[0], '\n')

            return jsonify({'keyword': item[0]})

    # No keyword found
    return jsonify({'keyword': ''})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
