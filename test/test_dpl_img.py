#!/usr/bin/env python
import argparse
import cv2
from datetime import datetime
import os
import numpy as np
import time
import json

parser = argparse.ArgumentParser(prog="Data creater")
parser.add_argument('--version', action='version', version='%(prog)s 1.1')
parser.add_argument('path', help="Picture to test ds script")
args = parser.parse_args()

def sd_checkboard(corners, CHECKERBOARD):
    sd = np.zeros(CHECKERBOARD[0] * CHECKERBOARD[1], np.float32)
    for n in xrange(CHECKERBOARD[0]):
        line = corners[n::CHECKERBOARD[0]]
        Y = np.array(list(map(lambda x: x[0][1],line.tolist())))
        X = np.array(list(map(lambda x: x[0][0],line.tolist())))
        N = len(X)

        k = (N*(X*Y).sum() - X.sum()*Y.sum())/(N*(X**2).sum() - X.sum()**2)
        b = (Y.sum() - k*X.sum())/N
        for j in xrange(CHECKERBOARD[1]):
            # Here I already know approx line y = kx + b, so I make right triangle
            # with side which parallel with axes. After that I found distance
            # from point to line use area of triangle 
            y = k*X[j] + b
            x = (Y[j]-b)/k
            side_b = np.absolute(X[j] - x)
            side_c = np.absolute(Y[j] - y)
            side_a = np.sqrt(side_b**2 + side_c**2)
            sd[n*CHECKERBOARD[1] + j] = side_b*side_c/side_a
    return sd.sum()/(CHECKERBOARD[0] * CHECKERBOARD[1])




def main():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    CHECKERBOARD = (6,9)
    frame = cv2.imread(args.path)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    ret, corners = cv2.findChessboardCorners(blurred, CHECKERBOARD, cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
    corners2 = cv2.cornerSubPix(blurred,corners,(11,11),(-1,-1),criteria)
    ## Add code for sd test
    print(sd_checkboard(corners2,CHECKERBOARD))
    cv2.imshow("test",frame)
    cv2.waitKey(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
