import math
import time
import threading

import imutils
from playsound import playsound
import cv2
import mediapipe as mp
import numpy as np
from math import sqrt


#playsound('/path/note.wav')


mp_drawing = mp.solutions.drawing_utils
myPose = mp.solutions.pose
poses = myPose.Pose()
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('http://192.168.191.2:8080/video')


def Trigger():
    playsound(r'sounds/beep.mp3')
    return

while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=800)
    results = poses.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        Head = results.pose_landmarks.landmark[0]
        rHands = results.pose_landmarks.landmark[18]
        lHands = results.pose_landmarks.landmark[17]
        Shol = results.pose_landmarks.landmark[12]

        # geetting center Hand coordinates
        eX = int(Head.x * frame.shape[1])
        eY = int(Head.y * frame.shape[0])

        # shoulder
        Sx = int(Shol.x * frame.shape[1])
        Sy = int(Shol.y * frame.shape[0])

        # getting RHand coordinates
        rhX = int(rHands.x * frame.shape[1])
        rhY = int(rHands.y * frame.shape[0])

        # getting LHand coordinates
        lhX = int(lHands.x * frame.shape[1])
        lhY = int(lHands.y * frame.shape[0])


        Radius = int(sqrt(((eX - Sx) * (eX - Sx)) + ((eY - Sy) * (eY - Sy))))
        rad=int(Radius*0.65)

        LRadius = int(sqrt(((eX - lhX) * (eX - lhX)) + ((eY - lhY) * (eY - lhY))))
        L_HRad=int(LRadius*0.70)

        RRadius = int(sqrt(((eX - rhX) * (eX - rhX)) + ((eY - rhY) * (eY - rhY))))
        R_HRad=int(RRadius*0.70)

        t1 = threading.Thread(target=Trigger)

        if R_HRad<=rad or L_HRad<=rad:
            t1.start()

        #Radius = 30
        #OffRadius = Radius - 10

        #cv2.circle(frame, (int(rhX), int(rhY)), Radius, (255, 76, 0), -1)
        #cv2.circle(frame, (int(lhX), int(lhY)), Radius, (255, 255, 0), -1)

        cv2.circle(frame, (int(eX), int(eY)), rad, (255, 76, 0), 1)






        # Distance
        # Halt = int(sqrt(((lhX - OfX) * (lhX - OfX)) + ((lhY - OfY) * (lhY - OfY))))

        # #Getting the angle
        Pone = results.pose_landmarks.landmark[11]
        Ptwo = results.pose_landmarks.landmark[13]
        Pthree = results.pose_landmarks.landmark[15]




        landmarks = results.pose_landmarks.landmark
        # np_landmarks = np.array([(lm.x, lm.y, lm.z, lm.visibility) for lm in landmarks])
        # print(np_landmarks)

        # mp_drawing.draw_landmarks(frame, results.pose_landmarks, myPose.POSE_CONNECTIONS)

    cv2.imshow('Cough detection', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
