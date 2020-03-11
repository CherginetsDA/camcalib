#!/usr/bin/env python

# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html

import argparse
import numpy as np
import sys
import cv2
import glob
import json

parser = argparse.ArgumentParser(prog="Find param")
parser.add_argument("path",help="Path to the picture set")
parser.add_argument("-v","--video",action="store_true",help="Test video on")
parser.add_argument("--version",action="version", version='%(prog)s 1.0')
args = parser.parse_args()



def save_to_conf(mtx, dist):
    print("Save koef to config file")
    # device_name = input("Enter name of device:  ")
    params = {"mtx":mtx, "dist":dist}
    with open("../../config/"+"device_name"+".json", 'w') as f:
        json.dump(params,f)



def get_image_names(folder_path):
    return glob.glob((folder_path if folder_path[-1] == '/' else folder_path + '/') + '*.jpg')

def images_reserch(images):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    print("Find " + str(len(images)) + ' images')

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(blurred, (6,9), cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)
    return objpoints,imgpoints,gray.shape[::-1]

def change_image_save(images, mtx, dist):
    for fname in images:
        img = cv2.imread(fname)
        h,  w = img.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imwrite(fname.replace('data','result'),dst)

def video_test(mtx, dist):
    if args.video:
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
        cap.set(3,600)
        cap.set(4,600)
        print("Done.")


        print("Press s to save coef")
        print("Press q to exit...")

        kin = 'a'

        while kin is not ord('q'):
            ret,frame = cap.read()
            if not ret == True:
                continue
            h,  w = frame.shape[:2]
            newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
            dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
            cv2.imshow('Camera Data', frame)
            kin = cv2.waitKey(1)
            if  kin == ord('s'):
                return True
    else:
        return True
    return False

def main():
    folder_path = sys.argv[1]
    print('Reserch images in ' + (folder_path if folder_path[-1] == '/' else folder_path + '/') + '...')

    images = get_image_names(folder_path)
    objpoints,imgpoints,shap = images_reserch(images)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    print("-"*25)
    print("Start calibration camera...")
    print(len(objpoints))
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,shap ,None,None)
    if ret:
        print("Done.")
    print("-"*25)
    if video_test(mtx, dist):
        print("-"*25)
        change_image_save(images, mtx, dist)
        # save_to_conf(mtx, dist)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
    # except:
    #     print("Something is wrong")

# TODO: check that folder exist in result/calibration folder
# TODO: add function for created config for device
