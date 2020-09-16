# Copyright (c) Ye Liu. All rights reserved.

import cv2


class ObjectRecognizer(object):

    def __init__(self, window_name, camera_idx):
        self.color = (0, 255, 0)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.window_name = window_name
        self.camera_idx = camera_idx

        self.faceClassifier = cv2.CascadeClassifier(
            '/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml'  # noqa
        )
        self.breadClassifier = cv2.CascadeClassifier(
            'Classifier/cascade_bread_18-8-13_11stages.xml')
        self.cupClassifier = cv2.CascadeClassifier(
            'Classifier/cascade_cup_18-8-16_6stages.xml')
        self.classifier = self.faceClassifier

    def catchUsbVideo(self):
        cv2.namedWindow(self.window_name, self.camera_idx)
        # cv2.resizeWindow(self.window_name, 100, 100)

        cap = cv2.VideoCapture(self.camera_idx)

        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                print('frame not found')
                break

            # Create gray level image
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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

                    cv2.putText(frame, '(%d,%d)' % (center_x, center_y),
                                (10, 30), self.font, 1, (255, 0, 255), 3)

                    cv2.rectangle(frame, (x - 10, y - 10),
                                  (x + w + 10, y + h + 10), self.color, 2)

                    cv2.putText(frame,
                                'Size: %d%%' % int(100 * h / frame.shape[0]),
                                (x + 5, y + 30), self.font, 1, (255, 0, 255),
                                3)

            # Show image
            cv2.imshow(self.window_name, frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def switchClassfier(self, classifier):
        if classifier == 'face':
            self.classifier = self.faceClassifier
        elif classifier == 'bread':
            self.classifier = self.breadClassifier
        elif classifier == 'water':
            self.classifier = self.cupClassifier
        else:
            print('classifier not found')
            return


if __name__ == '__main__':
    # 0 for original camera, 1 for webcam
    detector = ObjectRecognizer('ObjectRecognition', 0)
    detector.catchUsbVideo()
