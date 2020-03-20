#!/usr/bin/env python

import numpy as np
import argparse
import imutils
import cv2
import time

parser = argparse.ArgumentParser(prog="Data creater")
parser.add_argument('--version', action='version', version='%(prog)s 1.1')
parser.add_argument('path', help="Path for saving new picture")
args = parser.parse_args()

def main():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap.open()
        if not cap.isOpened():
            print("Can't find camera...")
            exit()
    print("Done.")

    kin = 'a'
    kkk = 150
    check_time = -1
    while kin is not ord('q'):
        time_s = time.time()
        ret,frame = cap.read()
        if not ret == True:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blurred, kkk, 255, cv2.THRESH_BINARY)[1]
        ret, corners = cv2.findChessboardCorners(thresh, (6,9), cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
        if ret:
            if check_time < 0:
                check_time=time.time()
            elif time_s - check_time > 15:
                filename = args.path
                if filename[-1] != '/':
                    filename +='/'
                cv2.imwrite(filename + time.strftime("%d%m%Y_%H%M%S", time.gmtime())+ str('.png'), frame)
                break
            cv2.putText(frame,"kkk: " + str(kkk),(10,30), cv2.FONT_HERSHEY_SIMPLEX,0.5,(200,100,150),2,cv2.LINE_AA)
            if time_s - check_time < 15:
                cv2.putText(frame,"to made image: "+ str(time_s - check_time) + " sec",(10,110),cv2.FONT_HERSHEY_SIMPLEX,0.5,(200,100,155),2,cv2.LINE_AA)
            cv2.putText(frame,"I SEE IT",(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(200,100,155),2,cv2.LINE_AA)
            cv2.putText(frame,"r to kkk += 1",(10,70),cv2.FONT_HERSHEY_SIMPLEX,0.5,(200,100,155),2,cv2.LINE_AA)
            cv2.putText(frame,"f to kkk -= 1",(10,90),cv2.FONT_HERSHEY_SIMPLEX,0.5,(200,100,155),2,cv2.LINE_AA)
            corners2 = cv2.cornerSubPix(blurred,corners,(11,11),(-1,-1),criteria)
            frame = cv2.drawChessboardCorners(frame, (6,9), corners2,ret)
        cv2.imshow('KKK',frame)
        cv2.imshow('Thresh',thresh)
        kin = cv2.waitKey(1)
        if kin == ord('r'):
            kkk+=10
        elif kin == ord('f'):
            kkk-=10

    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
