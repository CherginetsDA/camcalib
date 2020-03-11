#!/usr/bin/env python

import numpy as np
import argparse
import imutils
import cv2

parser = argparse.ArgumentParser(prog="Find param")
parser.add_argument("pict",help="The picture")
parser.add_argument("--version",action="version", version='%(prog)s 1.0')
args = parser.parse_args()

def main():
    # frame = cv2.imread("../../data/shapes/shapes.png")
    frame = cv2.imread(args.pict)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    cnts,contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # cnts,contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # print(len(cnts))
    cv2.drawContours(frame, contours, -1, (0,255,0), 3)
    ####
    # for c in cnts:
	# # compute the center of the contour
	# M = cv2.moments(c)
	# cX = int(M["m10"] / M["m00"])
	# cY = int(M["m01"] / M["m00"])
	# # draw the contour and center of the shape on the cnts
	# cv2.drawContours(cnts, [c], -1, (0, 255, 0), 2)
	# cv2.circle(cnts, (cX, cY), 7, (255, 255, 255), -1)
	# cv2.putText(cnts, "center", (cX - 20, cY - 20),
	# 	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
	# show the image
    cv2.imshow("Image", cnts)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
