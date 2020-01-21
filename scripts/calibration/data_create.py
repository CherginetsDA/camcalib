import cv2
from datetime import datetime
import os


# Well, this script for creating data set. You just start it, look at screen and you'll see data from your camera, just press S and this frame going to save in data/calibration/<data and time then it was created> folder.
# I hope I'll realized something much cooler then that (^.^)
def main():
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
    cap.set(3,1080)
    cap.set(4,720)
    print("Done.")

    path = os.getcwd() + '/../../data/calibration/' + datetime.now().strftime("%d%m%Y%H%M%S") + '/'
    os.mkdir(path)
    pictNumber = 1 if len(sys.argv) == 1 else sys.argv[1]


    print("Press s to save image")
    print("Press q to exit...")

    while(pictNumber < 26):
        ret,frame = cap.read()
        cv2.imshow('Camera Data', frame)

        kin = cv2.waitKey(1)

        if  kin == ord('s'):
            cv2.imwrite(path+str(pictNumber)+'.jpg',frame)
            print("Save picture number: " + str(pictNumber))
            pictNumber = pictNumber + 1
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
    except:
        print("Something is wrong")

## Maybe if save image in list and save in the end of program, it's can be more comfortable.
