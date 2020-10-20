#!/usr/bin/env python
import argparse
import cv2
import numpy as np
import json
import sys
import csv

parser = argparse.ArgumentParser(prog="Data creater")
parser.add_argument('--version', action='version', version='%(prog)s 1.1')
parser.add_argument('-c','--conf', nargs="?", help="Config name and path to  save params")
args = parser.parse_args()

def dpl_checkboard(corners, CHECKERBOARD):
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
            sd[n*CHECKERBOARD[1] + j] = np.absolute(Y[j] - k*X[j] - b)
    return sd.sum()/(CHECKERBOARD[0] * CHECKERBOARD[1])

def read_camera_param(filename='../config/cam_param.json'):
    config_file =open(filename,'r')
    content = json.loads(config_file.read())
    config_file.close()
    return np.array(content["matrix_cam_param"]),np.array(content['dist']),np.array(content['new_matrix_cam_param'])


def main():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    cap = cv2.VideoCapture(0)
    print("Opening camera...")
    if not cap.isOpened():
        cap.open()
        if not cap.isOpened():
            print("Can't find camera...")
            exit()
    print("Done.\n")
    print("Press q to exit...")

    mtx,dist,newcammtx = read_camera_param()
    kin = 'a'

    kkk = 150
    with open('../metrix_dpl_sd.csv', mode='w') as csv_file:
        csv_wr = csv.writer(csv_file,delimiter=',')
        while kin != ord('q'):
            ret,frame = cap.read()
            if ret == False:
                print("Problem with read from camera")
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            dst = cv2.undistort(blurred,mtx,dist, None,newcammtx)
            ret, corners = cv2.findChessboardCorners(blurred, (6,9), flags=cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
            # if ret:
            #     corners2 = cv2.cornerSubPix(blurred,corners,(11,11),(-1,-1),criteria)
            #     frame = cv2.drawChessboardCorners(frame, (6,9), corners2,ret)
            #     print(sd_checkboard(corners2, (6,9)))
            # ret, corners = cv2.findChessboardCorners(dst, (6,9), cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
            if ret:
                corners2 = cv2.cornerSubPix(dst,corners,(11,11),(-1,-1),criteria)
                dpl = dpl_checkboard(corners2, (6,9))
                sd = sd_checkboard(corners2, (6,9))
                csv_wr.writerow([dpl,sd])
                sys.stdout.write("\b")
                sys.stdout.write('Metric value %f\r' % dpl)
                sys.stdout.write('Metric value %f\r' % sd)
                sys.stdout.flush()
            # dst = cv2.undistort(frame,mtx,dist, None,newcammtx)
            # cv2.imshow('After calibration', dst)
            cv2.imshow('Camera Data', frame)
            kin = cv2.waitKey(1)

        cv2.destroyAllWindows()
        cap.release()

        print("Done.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
