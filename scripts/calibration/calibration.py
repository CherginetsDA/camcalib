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
parser.add_argument('-n','--numb', nargs="?", type=int, const=100, default=50, help="Count of pictures")
parser.add_argument('-s','--side', nargs="?", type=float, const=0.0285,default=1, help="Size of square")
parser.add_argument('-c','--conf', action="store_true", help="Config name and path to  save params")
args = parser.parse_args()


def save_camera_param(mtx,dist,newcammtx, filename='../../config/cam_param.json'):
    json_text = json.dumps({"matrix_cam_param":mtx.tolist(),'new_matrix_cam_param':newcammtx.tolist(),'dist':dist.tolist()})
    config_file =open(filename,'w')
    config_file.write(json_text)
    config_file.close()

def main():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    CHECKERBOARD = (6,9)
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)*args.side
    objpoints = []
    imgpoints = []

    cap = cv2.VideoCapture(0)
    print("Opening camera...")
    #check that camera is working
    if not cap.isOpened():
        cap.open()
        if not cap.isOpened():
            print("Can't find camera...")
            exit()
    print("Done.")

    print("Change image parameters...")
    # Set another size of capture
    print("Done.")
    pictNumber = args.numb
    pict = 1

    print("Press s to save image")
    print("Press q to exit...")
    check_time = time.time()
    while(pict < pictNumber):
        time_s = time.time()
        ret,frame = cap.read()
        if ret == False:
            print("Read from camera problem")
            continue
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        ret, corners = cv2.findChessboardCorners(blurred, CHECKERBOARD, cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)

        if ret:
            cv2.putText(frame,"I SEE IT",(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
            corners2 = cv2.cornerSubPix(blurred,corners,(11,11),(-1,-1),criteria)
            frame = cv2.drawChessboardCorners(frame, CHECKERBOARD, corners2,ret)
            if (time_s - check_time) > 0.25:
                objpoints.append(objp)
                imgpoints.append(corners2)
                pict += 1
                check_time = time_s

        cv2.putText(frame,"number of pict: " + str(pict),(10,30), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow('Camera Data', frame)

        kin = cv2.waitKey(1)

        if  kin == ord('q'):
            break
    h,w = frame.shape[:2]

    cv2.destroyAllWindows()
    print("Height is " + str(h))
    print("width is " + str(w))

    print("Start culculated")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print("Camera matrix : \n")
    print(mtx)
    print("dist : \n")
    print(dist)
    newcammtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    x,y,w,h = roi

    while kin != ord('q'):
        ret,frame = cap.read()
        if ret == False:
            print("Read from camera problem")
            continue
        dst = cv2.undistort(frame,mtx,dist, None,newcammtx)
        dst = dst[y:y+h, x:x+w]
        cv2.imshow('After calibration', dst)
        cv2.imshow('Camera Data', frame)
        kin = cv2.waitKey(1)
        if kin == ord('s'):
            save_camera_param(mtx,dist,newcammtx)
            # save_camera_param(mtx,dist,newcammtx,args.conf)
            break

    cap.release()

    print("Done.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
    # except:
    #     print("Something is wrong")

## Maybe if save image in list and save in the end of program, it's can be more comfortable.
