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


def detect_and_predict_mask(frame, faceNet, maskNet):
    (h, w) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                                 (104.0, 177.0, 123.0))

    faceNet.setInput(blob)
    detections = faceNet.forward()
    # print(detections.shape)
    # print(".")

    faces = []
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
            faces.append(face)
            locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)


prototxtPath = r'C:\Program Files\Innovation projects\CovidEnforcement\MaskCheck\Disease_OutBreak_Assistance\face_detector\deploy.prototxt'
weightsPath = r'C:\Program Files\Innovation projects\CovidEnforcement\MaskCheck\Disease_OutBreak_Assistance\face_detector\res10_300x300_ssd_iter_140000.caffemodel'
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

maskNet = load_model(r'C:\Program Files\Innovation projects\CovidEnforcement\MaskCheck\Disease_OutBreak_Assistance\mask_detector.model')

print("[INFO] Running...")
vs = VideoStream(src=0).start()

while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=800)

    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

    for (box, pred) in zip(locs, preds):
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        label = "Mask" if mask > withoutMask else "No Mask"
        textVisual = "Safe" if mask > withoutMask else "Not Safe"
        color = (100, 180, 0) if label == "Mask" else (0, 0, 255)

        # include the probability in the label
        textVisual = "{}: {:.2f}%".format(textVisual, max(mask, withoutMask) * 100)

        cv2.putText(frame, textVisual, (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

    cv2.imshow("UMat Glance", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
