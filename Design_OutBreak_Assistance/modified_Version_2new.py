# Adding the database feature

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream, FPS
import numpy as np
import imutils
import time
import cv2
import os
from playsound import playsound
import mediapipe as mp
from mylib import config, thread
from mylib.mailer import Mailer
from mylib.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import argparse, schedule
import sys
import matplotlib as mpl
import matplotlib.cm as mtpltcm
from datetime import datetime

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
    # print(".")

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

# ----------------------------Parse req. arguments------------------------------#
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
                help="path to (optional) input video file")
ap.add_argument("-o", "--output", type=str, default="",
                help="path to (optional) output video file")
ap.add_argument("-d", "--display", type=int, default=1,
                help="whether or not output frame should be displayed")
args = vars(ap.parse_args())
# ------------------------------------------------------------------------------#

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# derive the paths to the YOLO weights and model configuration
'''
weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])
'''
weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3-tiny.weights"])
configPath = os.path.sep.join([config.MODEL_PATH, "yolov3-tiny.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# check if we are going to use GPU
if config.USE_GPU:
    # set CUDA as the preferable backend and target
    print("")
    print("[INFO] Looking for GPU")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
writer = None
# start the FPS counter
fps = FPS().start()

# initialize the colormap
# colormap = mpl.cm.jet
colormap = mpl.cm.viridis_r
# colormap = mpl.cm.cool
cNorm = mpl.colors.Normalize(vmin=0, vmax=255)
scalarMap = mtpltcm.ScalarMappable(norm=cNorm, cmap=colormap)

while True:

    frame = vs.read()
    Meshed = vs.read()
    Dis_frame = vs.read()
    frame2 = vs.read()
    Mask = cv2.imread(no_mask)
    Distance = cv2.imread(no_distance)
    # mainView = cv2.imread("App Images/ape.png")
    frame = imutils.resize(frame, width=600)
    Meshed = imutils.resize(Meshed, width=600)
    Mask = imutils.resize(Mask, width=600)
    Distance = imutils.resize(Distance, width=600)
    Dis_frame = imutils.resize(Dis_frame, width=600)

    # -----------------------------------------Distance_started----------------------------------------------------------------------#
    Dis_results = detect_people(Dis_frame, net, ln,
                                personIdx=LABELS.index("person"))

    # initialize the set of indexes that violate the max/min social distance limits
    serious = set()
    abnormal = set()

    # ensure there are *at least* two people detections (required in
    # order to compute our pairwise distance maps)
    if len(Dis_results) >= 2:
        # extract all centroids from the results and compute the
        # Euclidean distances between all pairs of the centroids
        centroids = np.array([r[2] for r in Dis_results])
        D = dist.cdist(centroids, centroids, metric="euclidean")

        # loop over the upper triangular of the distance matrix
        for i in range(0, D.shape[0]):
            for j in range(i + 1, D.shape[1]):
                # check to see if the distance between any two
                # centroid pairs is less than the configured number of pixels
                if D[i, j] < config.MIN_DISTANCE:
                    # update our violation set with the indexes of the centroid pairs
                    serious.add(i)
                    serious.add(j)
                # update our abnormal set if the centroid distance is below max distance limit
                if (D[i, j] < config.MAX_DISTANCE) and not serious:
                    abnormal.add(i)
                    abnormal.add(j)

    # loop over the results
    for (i, (prob, bbox, centroid)) in enumerate(Dis_results):
        # extract the bounding box and centroid coordinates, then
        # initialize the color of the annotation
        (startX, startY, endX, endY) = bbox
        (cX, cY) = centroid
        color = (0, 255, 0)

        # if the index pair exists within the violation/abnormal sets, then update the color
        if i in serious:
            color = (0, 0, 255)
        elif i in abnormal:
            color = (0, 255, 255)  # orange = (0, 165, 255)

        # draw (1) a bounding box around the person and (2) the
        # centroid coordinates of the person,
        cv2.rectangle(Dis_frame, (startX, startY), (endX, endY), color, 2)
        cv2.circle(Dis_frame, (cX, cY), 5, color, 2)

    # draw some of the parameters
    Safe_Distance = "Safe distance: >{} px".format(config.MAX_DISTANCE)
    # cv2.putText(frame, Safe_Distance, (470, frame.shape[0] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 0, 0), 2)
    Threshold = "Threshold limit: {}".format(config.Threshold)
    # cv2.putText(frame, Threshold, (470, frame.shape[0] - 50),cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 0, 0), 2)

    # draw the total number of social distancing violations on the output frame
    text = "High: {}".format(len(serious))
    # cv2.putText(frame, text, (10, frame.shape[0] - 55),cv2.FONT_HERSHEY_SIMPLEX, 0.70, (0, 0, 255), 2)

    text1 = "Medium: {}".format(len(abnormal))
    # cv2.putText(frame, text1, (10, frame.shape[0] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.70, (0, 255, 255), 2)

    # ------------------------------Alert function----------------------------------#
    if len(serious) >= config.Threshold:
        cv2.putText(Dis_frame, "-ALERT: Violations over limit-", (10, Dis_frame.shape[0] - 80),
                    cv2.FONT_HERSHEY_COMPLEX, 0.60, (0, 0, 255), 2)
        if config.ALERT:
            print("")
            print('[INFO] Sending mail...')
            # Mailer().send(config.MAIL)
            print('[INFO] Mail sent')
    # config.ALERT = False
    # ------------------------------------------------------------------------------#
    # check to see if the output frame should be displayed to our screen
    if args["display"] > 0:
        # show the output frame
        cv2.imshow("UMAT GLANCE", Dis_frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    # update the FPS counter
    fps.update()

    # if an output video file path has been supplied and the video
    # writer has not been initialized, do so now
    if args["output"] != "" and writer is None:
        # initialize our video writer
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(args["output"], fourcc, 25,
                                 (Dis_frame.shape[1], Dis_frame.shape[0]), True)

    # if the video writer is not None, write the frame to the output video file
    if writer is not None:
        writer.write(Dis_frame)

    # ---------------------------------------Distance_Ended------------------------------------------------------------------------#

    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

    detect_and_predict_mask(frame, faceNet, maskNet)
    num = "0" if len(detect_and_predict_mask.faces) < 1 else "1"

    if num == "0":
        print("not found")

        no_mask = r"App images/no_detection.jpg"

    for (box, pred) in zip(locs, preds):
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        label = "Mask" if mask > withoutMask else "No Mask"
        textVisual = "Safe" if mask > withoutMask else "Not Safe"
        color = (100, 180, 0) if label == "Mask" else (0, 0, 255)
        # ####################################Sound##########################################################################
        # if label == "No Mask":
        #    playsound('testsoundF.mp3')

        # playsound('sound/mask_sound_long.mp3')
        # ##################################################################################################################
        # include the probability in the label

        ################################################################################################
        if num == "0":
            no_mask = r"App images/no_detection.jpg"
        if textVisual == "Not Safe":
            no_mask = r"App images/no_mask.jpg"
            # Capture face when there is no face mask
            TimeStamp = datetime.now().strftime('%Y%m%d%H%M%S')
            img_name = "{}.png".format(TimeStamp)
            # cv2.imwrite(img_name, frame)

            ROI = frame[startY:endY, startX:endX].copy()

            path = r"C:\Users\Julius Anumbia\Desktop\CovidEnforcement\MaskCheck\MaskCheck\Pictures"
            cv2.imwrite(os.path.join(path, img_name), ROI)
            print("{} Saved".format(img_name))

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

    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (15, 15), 0)

    colors = scalarMap.to_rgba(blur, bytes=False)

    # Display the resulting frame
    cv2.imshow('Temperature Check', colors)
    cv2.imshow("UMat Glance", frame)
    cv2.imshow("Meshed", Meshed)
    cv2.imshow("Mask Check", Mask)
    cv2.imshow("Distance", Distance)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
# stop the timer and display FPS information

fps.stop()
cv2.destroyAllWindows()
vs.stop()
