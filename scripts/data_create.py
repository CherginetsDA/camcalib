import cv2
from datetime import datetime
import os


# Well, this script for creating data set. You just start it, look at screen and it you are pritty like that you see, just press S and this frame going to save in data/calibration/<data and time then it was created> folder.
# I hope I'll realized something much cooler then that (^.^)
def main():
    print("Press s to save image")
    print("Press q to exit...")
    cap = cv2.VideoCapture(0)

    #check that camera is working
    if not cap.isOpened():
        cap.open()
        if not cap.isOpened():
            print("Can't find camera...")
            exit()
    # Set another size of capture
    cap.set(3,1080)
    cap.set(4,720)

    path = os.getcwd() + '/../data/calibration/' + datetime.now().strftime("%d%m%Y%H%M%S") + '/'
    os.mkdir(path)
    pictNumber = 1

    while(pictNumber < 26):
        ret,frame = cap.read()
        cv2.imshow('Camera Test', frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(path+str(pictNumber)+'.jpg',frame)
            print("Save picture number: " + str(pictNumber))
            pictNumber = pictNumber + 1


    cap.release()
    cv2.destroyAllWindows()
    print("Done.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except:
        print("Something is wrong")
