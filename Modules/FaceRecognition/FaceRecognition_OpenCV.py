#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import serial


class FaceRecognition(object):

    def __init__(self, window_name, camera_idx):
        self.color = (0, 255, 0)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.window_name = window_name

        cv2.namedWindow(window_name, 0)
        # cv2.resizeWindow(window_name, 100, 100)

        self.cap = cv2.VideoCapture(camera_idx)
        self.classfier = cv2.CascadeClassifier(
            "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")

        # self.classfier = cv2.CascadeClassifier(
        #     "/Volumes/Data/CNN/data/cascade.xml")

        # self.ser = serial.Serial('/dev/cu.usbmodem14141', 9600)

    def CatchUsbVideo(self):
        while self.cap.isOpened():
            ok, frame = self.cap.read()
            if not ok:
                print('frame not found')
                break

            # Create gray level image
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Face recognition
            faceRects = self.classfier.detectMultiScale(
                grey, scaleFactor=1.3, minNeighbors=3, minSize=(32, 32))

            if len(faceRects) > 0:
                for (x, y, w, h) in faceRects:
                    center_x = x + w / 2
                    center_y = y + h / 2

                    print(center_x, frame.shape[0] / 2)

                    # if center_x <= frame.shape[1] / 2:
                    #     self.ser.write('r'.encode())
                    # else:
                    #     self.ser.write('l'.encode())

                    # line = self.ser.readline()
                    # print(line.decode())

                    cv2.putText(frame, '(%d,%d)' % (center_x, center_y),
                                (10, 30), self.font, 1, (255, 0, 255), 3)

                    cv2.rectangle(frame, (x - 10, y - 10),
                                  (x + w + 10, y + h + 10), self.color, 2)

                    cv2.putText(frame, 'Size: %d%%' % int(
                        100 * h / frame.shape[0]), (x + 5, y + 30), self.font, 1, (255, 0, 255), 3)

            # Show image
            cv2.imshow(self.window_name, frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # 0 for original camera, 1 for webcam
    detector = FaceRecognition("FaceRecognition", 0)
    detector.CatchUsbVideo()
