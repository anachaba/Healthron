import os

import cv2
import numpy as np

cam = cv2.VideoCapture(0)

if not cam.isOpened():
  print ("Could not open cam")
  exit()

while(1):
    ret, frame = cam.read()
    if ret:
        frame = cv2.flip(frame,1)
        display = cv2.rectangle(frame.copy(),(300,150),(500,400),(0,255,0),2)
        cv2.imshow('curFrame',display)


        ROI = frame[150:400, 300:500].copy()
        path = r"C:\Users\Julius Anumbia\Desktop\CovidEnforcement\MaskCheck\MaskCheck\Pictures"
        cv2.imwrite(os.path.join(path, 'img_name.png'), ROI)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()