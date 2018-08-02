#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2


def CatchUsbVideo(window_name, camera_idx):
    cv2.namedWindow(window_name)

    cap = cv2.VideoCapture(camera_idx)

    classfier = cv2.CascadeClassifier(
        "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")

    # 识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)

    while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:
            break

        # 将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 人脸检测，1.2 和 2 分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier.detectMultiScale(
            grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects) > 0:  # 大于 0 则检测到人脸
            for (x, y, w, h) in faceRects:  # 单独框出每一张人脸
                cv2.rectangle(frame, (x - 10, y - 10),
                              (x + w + 10, y + h + 10), color, 2)

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, '%d%%' % int(
                    100 * h / frame.shape[0]), (x + 10, y + 30), font, 1, (255, 0, 255), 4)

        # 显示图像
        cv2.imshow(window_name, frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # 释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    CatchUsbVideo("FaceRecognition", 1)
