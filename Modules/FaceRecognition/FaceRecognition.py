#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2


def CatchUsbVideo(window_name, camera_idx):
    cv2.namedWindow(window_name)

    cap = cv2.VideoCapture(camera_idx)

    classfier = cv2.CascadeClassifier(
        "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")

    # Frame color
    color = (0, 255, 0)

    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            print('frame not found')
            break

        # Create gray level image
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Face recognition
        faceRects = classfier.detectMultiScale(
            grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))

        if len(faceRects) > 0:
            for (x, y, w, h) in faceRects:
                cv2.rectangle(frame, (x - 10, y - 10),
                              (x + w + 10, y + h + 10), color, 2)

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'Size: %d%%' % int(
                    100 * h / frame.shape[0]), (x + 5, y + 30), font, 1, (255, 0, 255), 3)

        # Show image
        cv2.imshow(window_name, frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    CatchUsbVideo("FaceRecognition", 1)  # 0 for original camera, 1 for webcam
