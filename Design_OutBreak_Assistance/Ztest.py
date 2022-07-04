###     Distance test code
import math
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
myPose = mp.solutions.pose
poses = myPose.Pose()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = poses.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    if results.pose_landmarks:
        Head = results.pose_landmarks.landmark[0]

        # geetting center Hand coordinates
        eX = int(Head.x * frame.shape[1])
        eY = int(Head.y * frame.shape[0])

        landmarks = results.pose_landmarks.landmark
        # np_landmarks = np.array([(lm.x, lm.y, lm.z, lm.visibility) for lm in landmarks])
        # print(np_landmarks)

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, myPose.POSE_CONNECTIONS)

    cv2.imshow('Distance detection', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
