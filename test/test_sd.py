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

def main():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    CHECKERBOARD = (6,9)
    frame = cv2.imread(args.path)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    ret, corners = cv2.findChessboardCorners(blurred, CHECKERBOARD, cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
    corners2 = cv2.cornerSubPix(blurred,corners,(11,11),(-1,-1),criteria)
    ## Add code for sd test
    cv2.imshow("test",frame)
    cv2.waitKey(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
