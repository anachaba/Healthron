import cv2
from imutils.video import VideoStream
from multiprocessing import Process

vs = VideoStream(0).start()
def start_1():
    while True:


        frame = vs.read()
        cv2.imshow('hello one', frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break




if __name__=='__main__':
    s1=Process(target=start_1)
    s1.start()
