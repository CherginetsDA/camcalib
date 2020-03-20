import cv2
import numpy as np
import json
import time

class calibration:
    def __init__(self,board_size=(6,9),pict = 150,conf='../../config/cam_param.json',side=0.0285):
        self.CHECKERBOARD = board_size
        self.objpoints = []
        self.imgpoints = []
        self.pictNumber = pict
        self.conf_name = conf
        self.side = side

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
        print("Done.")

    def save_camera_param(self):
        json_text = json.dumps({"matrix_cam_param":self.mtx.tolist(),'new_matrix_cam_param':self.newcammtx.tolist(),'dist':dist.tolist()})
        config_file =open(self.conf_name,'w')
        config_file.write(json_text)
        config_file.close()

    def data_set_create(self):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        objp = np.zeros((1, self.CHECKERBOARD[0] * self.CHECKERBOARD[1], 3), np.float32)
        objp[0,:,:2] = np.mgrid[0:self.CHECKERBOARD[0], 0:self.CHECKERBOARD[1]].T.reshape(-1, 2)*self.side
        print("\nPress s to save image")
        print("Press q to exit...")
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
                corners2 = cv2.cornerSubPix(blurred,corners,(11,11),(-1,-1),criteria)
                frame = cv2.drawChessboardCorners(frame, self.CHECKERBOARD, corners2,ret)
                if (time_s - check_time) > 0.25:
                    self.objpoints.append(objp)
                    self.imgpoints.append(corners2)
                    pict += 1
                    check_time = time_s

            cv2.putText(frame,"number of pict: " + str(pict),(10,30), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
            cv2.imshow('Camera Data', frame)

            kin = cv2.waitKey(1)

            if  kin == ord('q'):
                break
        h,w = frame.shape[:2]

        cv2.destroyAllWindows()
        print("\nHeight is " + str(h))
        print("width is " + str(w))

        print("\nStart culculated")
        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, gray.shape[::-1], None, None)
        print("\nCamera matrix : \n")
        print(self.mtx)
        print("\ndist : \n")
        print(self.dist)
        self.newcammtx, self.roi = cv2.getOptimalNewCameraMatrix(self.mtx,self.dist,(w,h),1,(w,h))

    def test_calib(self):
        x,y,w,h = self.roi
        kin = 'a'
        while kin != ord('q'):
            ret,frame = self.cap.read()
            if ret == False:
                print("Read from camera problem")
                continue
            dst = cv2.undistort(frame,self.mtx,self.dist, None,self.newcammtx)
            dst = dst[y:y+h, x:x+w]
            cv2.imshow('After calibration', dst)
            cv2.imshow('Camera Data', frame)
            kin = cv2.waitKey(1)
            if kin == ord('s'):
                self.save_camera_param(self.mtx,self.dist,self.newcammtx)
                # save_camera_param(mtx,dist,newcammtx,args.conf)
                break


    def camera_close(self):
        self.cap.release()
