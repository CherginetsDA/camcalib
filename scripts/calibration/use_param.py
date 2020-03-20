#!/usr/bin/env python
import argparse
import cv2
import numpy as np
import json

parser = argparse.ArgumentParser(prog="Data creater")
parser.add_argument('--version', action='version', version='%(prog)s 1.1')
parser.add_argument('-c','--conf', nargs="?", help="Config name and path to  save params")
args = parser.parse_args()


def read_camera_param(filename='../../config/cam_param.json'):
    config_file =open(filename,'r')
    content = json.loads(config_file.read())
    config_file.close()
    return np.array(content["matrix_cam_param"]),np.array(content['dist']),np.array(content['new_matrix_cam_param'])


def main():

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

    while kin != ord('q'):
        ret,frame = cap.read()
        if ret == False:
            print("Read from camera problem")
            continue
        dst = cv2.undistort(frame,mtx,dist, None,newcammtx)
        cv2.imshow('After calibration', dst)
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
