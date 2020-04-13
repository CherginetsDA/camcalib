import cv2
import numpy as np
import json
import time
import sys

DISTANCE_POINT_TO_LINE = 1

def print_line(n=80):
    print("-"*n)

class calibration:
    def __init__(self,board_size=(6,9),pict = 150,conf='../../config/cam_param.json',side=0.0285):
        print("The calibration settings:\n")
        line_size = 40+1+len(conf)+5
        print_line(line_size)
        print("%-40s %d"%("Count of pictures for data set: ", pict))
        print("%-40s (%d,%d)"%("Board size: ",board_size[0],board_size[1]))
        print("%-40s %f"%("Size the side of board's square: ",side))
        print("%-40s %s"%("Path to config file: ",conf))
        print_line(line_size)
        print("")
        self.CHECKERBOARD = board_size
        self.objpoints = []
        self.imgpoints = []
        self.pictNumber = pict
        self.conf_name = conf
        self.side = side
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def calibrate(self):
        self.camera_open()
        self.data_set_create()
        self.test_calib()
        self.camera_close()

    def camera_open(self):
        self.cap = cv2.VideoCapture(0)
        print("Opening camera...")
        #check that camera is working
        if not self.cap.isOpened():
            self.cap.open()
            if not self.cap.isOpened():
                print("Can't find camera...")
                exit()
        print("Done.\n")

    def save_camera_param(self):
        json_text = json.dumps({"matrix_cam_param":self.mtx.tolist(),'new_matrix_cam_param':self.newcammtx.tolist(),'dist':self.dist.tolist()})
        config_file =open(self.conf_name,'w')
        config_file.write(json_text)
        config_file.close()

    def data_set_create(self):

        objp = np.zeros((1, self.CHECKERBOARD[0] * self.CHECKERBOARD[1], 3), np.float32)
        objp[0,:,:2] = np.mgrid[0:self.CHECKERBOARD[0], 0:self.CHECKERBOARD[1]].T.reshape(-1, 2)*self.side
        print("Press c to finish making data set")
        print("Press e to exit...")
        pict = 0
        check_time = time.time()
        while(pict < self.pictNumber):
            time_s = time.time()
            ret,frame = self.cap.read()
            if ret == False:
                print("Read from camera problem")
                continue
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            ret, corners = cv2.findChessboardCorners(blurred, self.CHECKERBOARD, cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)

            if ret:
                cv2.putText(frame,"I SEE IT",(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
                corners2 = cv2.cornerSubPix(blurred,corners,(11,11),(-1,-1),self.criteria)
                frame = cv2.drawChessboardCorners(frame, self.CHECKERBOARD, corners2,ret)
                if (time_s - check_time) > 0.25:
                    self.objpoints.append(objp)
                    self.imgpoints.append(corners2)
                    pict += 1
                    check_time = time_s

            cv2.putText(frame,"number of pict: " + str(pict),(10,30), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
            cv2.imshow('Camera Data', frame)

            kin = cv2.waitKey(1)

            if  kin == ord('e'):
                print("exit")
                exit()
            elif kin == ord('c'):
                print("Interrupt making data set")
                break
        h,w = frame.shape[:2]

        cv2.destroyAllWindows()
        print("%-40s %d"%("\nHeight of the picture frame: ",h))
        print("%-40s %d"%("\nWidth of the picture frame: ",w))

        print("\nStart culculated")
        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, gray.shape[::-1], None, None)
        print("Done.\n")
        print_line()
        print("Camera matrix : \n")
        print(self.mtx)
        print("\nDistorsion coefficients: \n")
        print(self.dist)
        print_line()
        self.newcammtx, self.roi = cv2.getOptimalNewCameraMatrix(self.mtx,self.dist,(w,h),1,(w,h))

    def distance_point_to_line_metric(self,corners):
        sd = np.zeros(self.CHECKERBOARD[0] * self.CHECKERBOARD[1], np.float32)
        for n in xrange(self.CHECKERBOARD[0]):
            line = corners[n::self.CHECKERBOARD[0]]
            Y = np.array(list(map(lambda x: x[0][1],line.tolist())))
            X = np.array(list(map(lambda x: x[0][0],line.tolist())))
            N = len(X)

            k = (N*(X*Y).sum() - X.sum()*Y.sum())/(N*(X**2).sum() - X.sum()**2)
            b = (Y.sum() - k*X.sum())/N
            for j in xrange(self.CHECKERBOARD[1]):
                # Here I already know approx line y = kx + b, so I make right triangle
                # with side which parallel with axes. After that I found distance
                # from point to line use area of triangle
                y = k*X[j] + b
                x = (Y[j]-b)/k
                side_b = np.absolute(X[j] - x)
                side_c = np.absolute(Y[j] - y)
                side_a = np.sqrt(side_b**2 + side_c**2)
                sd[n*self.CHECKERBOARD[1] + j] = side_b*side_c/side_a
        return sd.sum()/(self.CHECKERBOARD[0] * self.CHECKERBOARD[1])

    def use_metric(self,frame,metric):
        if metric == DISTANCE_POINT_TO_LINE:
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            ret, corners = cv2.findChessboardCorners(blurred, self.CHECKERBOARD, cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
            if ret:
                cv2.putText(frame,"I SEE IT",(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
                corners2 = cv2.cornerSubPix(blurred,corners,(11,11),(-1,-1),self.criteria)
                sys.stdout.write("\b")
                sys.stdout.write('Metric value: %f\r' % self.distance_point_to_line_metric(corners2))
                sys.stdout.flush()

    def test_calib(self):
        print("Test calculated params")
        x,y,w,h = self.roi
        kin = 'a'
        print("\nPress s to save params")
        print("Press e to exit...\n")
        while kin != ord('e'):
            ret,frame = self.cap.read()
            if ret == False:
                print("Read from camera problem")
                continue
            dst = cv2.undistort(frame,self.mtx,self.dist, None,self.newcammtx)
            dst = dst[y:y+h, x:x+w]
            cv2.imshow('After calibration', dst)
            self.use_metric(dst,DISTANCE_POINT_TO_LINE)
            kin = cv2.waitKey(1)
            if kin == ord('s'):
                print("Save params")
                self.save_camera_param()
                break

    def camera_close(self):
        self.cap.release()
