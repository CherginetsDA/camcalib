#!/usr/bin/env python
import argparse
import cv2
from datetime import datetime
import os
import time

parser = argparse.ArgumentParser(prog="Data creater")
parser.add_argument('--version', action='version', version='%(prog)s 1.1')
parser.add_argument('-H','--height', nargs="?", type=int, const=720, default=600, help="Set height of frame (pixels)")
parser.add_argument('-W','--width', nargs="?", type=int, const=1080, default=600, help="Set width of frame (pixels)")
parser.add_argument('-n','--numb', nargs="?", type=int, const=25, default=1, help="Count of pictures")
parser.add_argument('-c','--check', action="store_true", help="Check that algoritm can find chess board")
# parser.add_argument('-e','--extension', nargs="2", type=int ,default=[7,6], help="Extansion of kalibration plate")
# TODO: add argparse for extention of chess board
args = parser.parse_args()

# Well, this script for creating data set. You just start it, look at screen and you'll see data from your camera, just press S and this frame going to save in data/calibration/<data and time then it was created> folder.
# I hope I'll realized something much cooler then that (^.^)
def main():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
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
    cap.set(3,args.width)
    cap.set(4,args.height)
    print("Done.")

    path = os.getcwd() + '/../../data/calibration/' + datetime.now().strftime("%d%m%Y%H%M%S") + '/'
    os.mkdir(path)
    pictNumber = args.numb
    pict = 0

    print("Press s to save image")
    print("Press q to exit...")

    while(pict < pictNumber):
        ret,frame = cap.read()
        if not ret == True:
            continue
        if args.check:
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            ret, corners = cv2.findChessboardCorners(blurred, (6,9), cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)

            if ret:
                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                cv2.imwrite(path+str(pict)+'.jpg',frame)
                frame = cv2.drawChessboardCorners(frame, (6,9), corners2,ret)
                print("Save picture number: " + str(pict))
                pict += 1
                time.sleep(0.1)

        cv2.putText(frame,"number of pict: " + str(pict),(10,30), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow('Camera Data', frame)


        kin = cv2.waitKey(1)

        if  kin == ord('s'):
            cv2.imwrite(path+str(pict)+'.jpg',frame)
            print("Save picture number: " + str(pictNumber))
            pict = pict + 1
        elif kin == ord('q'):
            break



    cap.release()
    cv2.destroyAllWindows()
    print("Done.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
    # except:
    #     print("Something is wrong")

## Maybe if save image in list and save in the end of program, it's can be more comfortable.
