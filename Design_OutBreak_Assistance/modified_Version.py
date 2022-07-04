# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
from playsound import playsound
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=5)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

no_mask = r"App images/no_detection.jpg"
no_distance = r"App images/no_distance.jpg"



def detect_and_predict_mask(frame, faceNet, maskNet):
    (h, w) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                                 (104.0, 177.0, 123.0))

    faceNet.setInput(blob)
    detections = faceNet.forward()
    # print(detections.shape)
    #print(".")

    detect_and_predict_mask.faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        if confidence > 0.4:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            # add the face and bounding boxes to their respective
            # lists
            detect_and_predict_mask.faces.append(face)
            locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detected
    if len(detect_and_predict_mask.faces) > 0:
        detect_and_predict_mask.faces = np.array(detect_and_predict_mask.faces, dtype="float32")
        preds = maskNet.predict(detect_and_predict_mask.faces, batch_size=32)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)




prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

maskNet = load_model("mask_detector.model")

print("[INFO] Running...")
vs = VideoStream(src=0).start()



while True:



    frame = vs.read()
    Meshed = vs.read()
    Mask = cv2.imread(no_mask)
    Distance = cv2.imread(no_distance)
    # mainView = cv2.imread("App Images/ape.png")
    frame = imutils.resize(frame, width=600)
    Meshed = imutils.resize(Meshed, width=600)
    Mask = imutils.resize(Mask, width=600)
    Distance = imutils.resize(Distance, width=600)



    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

    detect_and_predict_mask(frame,faceNet, maskNet)
    num = "0" if len(detect_and_predict_mask.faces)<1 else "1"

    if num =="0":
        print("not found")
        no_mask = r"App images/no_detection.jpg"





    for (box, pred) in zip(locs, preds):
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred










        label = "Mask" if mask > withoutMask else "No Mask"
        textVisual = "Safe" if mask > withoutMask else "Not Safe"
        color = (100, 180, 0) if label == "Mask" else (0, 0, 255)
        #####################################Sound##########################################################################
        # if label == "No Mask":
        #    playsound('testsoundF.mp3')

        # playsound('sound/mask_sound_long.mp3')
        ###################################################################################################################
        # include the probability in the label

        ################################################################################################
        if num == "0":
            no_mask = r"App images/no_detection.jpg"
        if textVisual == "Not Safe":
            no_mask = r"App images/no_mask.jpg"
        if textVisual == "Safe":
            no_mask = r"App images/yes_mask.jpg"




        textVisual = "{}: {:.2f}%".format(textVisual, max(mask, withoutMask) * 100)

        cv2.putText(frame, textVisual, (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

    imgRGB = cv2.cvtColor(Meshed, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(Meshed, faceLms, mpFaceMesh.FACE_CONNECTIONS, drawSpec, drawSpec)

    #cv2.imshow("UMat Glance", frame)
    #cv2.imshow("Meshed", Meshed)
    cv2.imshow("Mask Check", Mask)
    #cv2.imshow("Distance", Distance)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
