# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
import numpy as np
import sys
import cv2
import glob

def save_to_conf():
    print("Save koef to config file")

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

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

        # If found, add object points, image points (after refining them)

        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            # img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
            # cv2.imshow('img',img)
            # cv2.waitKey(500)
    return objpoints,imgpoints,gray.shape[::-1]

def change_image_save(images, mtx, dist):
    for fname in images:
        img = cv2.imread(fname)
        h,  w = img.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

        # undistort
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

        # crop the image
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imwrite(fname.replace('data','result'),dst)

# termination criteria
def main():
    folder_path = sys.argv[1]
    print('Reserch images in ' + (folder_path if folder_path[-1] == '/' else folder_path + '/') + '...')

    images = get_image_names(folder_path)
    objpoints,imgpoints,shap = images_reserch(images)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)

    print("Start calibration camera...")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,shap ,None,None)
    if ret: print("Done.")

    change_image_save(images, mtx, dist)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            main()
        else:
            print("Use: python find_param.py <data folder path>")
    except KeyboardInterrupt:
        exit()
    # except:
    #     print("Something is wrong")

# TODO: check that folder exist in result/calibration folder
