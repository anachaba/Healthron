import cv2
import mediapipe as mp
import time

from imutils.video import VideoStream

vs = VideoStream(src=0).start()
pTime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)

while True:
    img = vs.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            # nose= faceLms(10, 338)

            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACE_CONNECTIONS)


    cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime
    # cv2.putText(img, f' FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.imshow('Image', img)
    cv2.waitKey(1)
