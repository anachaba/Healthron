import math
import time
import threading

import imutils
from playsound import playsound
import cv2
import mediapipe as mp
import numpy as np
from math import sqrt

mp_drawing = mp.solutions.drawing_utils
myPose = mp.solutions.pose
poses = myPose.Pose()
cap = cv2.VideoCapture(0)


# cap = cv2.VideoCapture('http://192.168.191.2:8080/video')


def Trigger():
    # playsound(r'sounds/beep.mp3')
    print('s')
    return


scan = ['Scanning .', 'Scanning ..', ' Scanning ...', 'Scanning ....', 'Scanning .', ' Scanning ..', 'Scanning ...',
        ' Scanning ....', 'Scanning .', 'Scanning ..']

scan_val = 0


def scan_val_controller():
    global scan_val
    while True:

        for i in range(0, 8, 1):
            scan_val = i
            print(scan_val)
        for i in range(8, 0, -1):
            scan_val = i
            print(scan_val)


t1 = threading.Thread(target=scan_val_controller)
t1.start()
while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=800)
    results = poses.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        Head = results.pose_landmarks.landmark[0]
        Face_part = results.pose_landmarks.landmark[3]
        rHands = results.pose_landmarks.landmark[18]

        first_text = int(Head.x * frame.shape[1] * 12345)

        sencond_text = int(Face_part.x * frame.shape[1] * 1345)

        # font
        font = cv2.FONT_HERSHEY_SIMPLEX

        MOV_POS1x = int(Head.x * frame.shape[1])
        MOV_POS1y = int(Head.y * frame.shape[1])

        # org
        org = (MOV_POS1x - 300, MOV_POS1y - 150)
        org2 = (MOV_POS1x - 300, MOV_POS1y - 100)
        org3 = (MOV_POS1x - 300, MOV_POS1y - 50)

        # fontScale
        fontScale = 1

        # Blue color in BGR
        color = (255, 229, 204)
        color2 = (255, 255, 0)

        disease_color = (51, 255, 128)

        # Line thickness of 2 px
        thickness = 2

        # Using cv2.putText() method
        frame = cv2.putText(frame, str(first_text), org, font,
                            fontScale, color, thickness, cv2.LINE_AA)

        # Using cv2.putText() method
        frame = cv2.putText(frame, str(sencond_text), org2, font,
                            fontScale, color2, thickness, cv2.LINE_AA)

        # Using cv2.putText() method

        frame = cv2.putText(frame, str(scan[scan_val]), org3, font,
                            fontScale, disease_color, thickness, cv2.LINE_AA)

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, myPose.POSE_CONNECTIONS)

    cv2.imshow('Composure', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
