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
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg





class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")

        #
        self.setLayout(qtw.QVBoxLayout())

        # Text
        my_label = qtw.QLabel("Covid-19 System")
        my_label.setFont(qtg.QFont('Helvetica', 18))
        self.layout().addWidget(my_label)

        # Start Mask
        Mask_B = qtw.QPushButton("Mask", clicked = lambda: S_mask())
        self.layout().addWidget(Mask_B)

        # Start Mask
        Distance_B = qtw.QPushButton("Distance", clicked=lambda: S_distance())
        self.layout().addWidget(Distance_B)

        #Start Thermo
        # Start Mask
        Thermo_B = qtw.QPushButton("Thermo", clicked=lambda: S_thermo())
        self.layout().addWidget(Thermo_B)

        #My functions
        def S_distance():
            cv2.destroyAllWindows()
            for i in range(1, 5):
                cv2.waitKey(1)
            import MaskCheck.F_DISTANCE

        def S_mask():
            cv2.destroyAllWindows()
            for i in range(1, 5):
                cv2.waitKey(1)
            import MaskCheck.F_MASK

        def S_thermo():
            cv2.destroyAllWindows()
            for i in range(1, 5):
                cv2.waitKey(1)
            import MaskCheck.F_THERMO

        self.show()


app = qtw.QApplication([])
mw = MainWindow()

# Start App
app.exec_()

