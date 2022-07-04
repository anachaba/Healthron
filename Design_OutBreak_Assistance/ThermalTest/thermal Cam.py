import sys
import numpy as np
import cv2
import matplotlib as mpl
import matplotlib.cm as mtpltcm


def main(argv):
    cap = cv2.VideoCapture(0)

    # initialize the colormap
    # colormap = mpl.cm.jet
    colormap = mpl.cm.viridis_r
    # colormap = mpl.cm.cool
    cNorm = mpl.colors.Normalize(vmin=0, vmax=255)
    scalarMap = mtpltcm.ScalarMappable(norm=cNorm, cmap=colormap)

    while (True):

        ret, frame2 = cap.read()

        gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (15, 15), 0)

        colors = scalarMap.to_rgba(blur, bytes=False)

        # Display the resulting frame
        cv2.imshow('Temperature Check', colors)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
