#!/usr/bin/env python3
import argparse
import cv2

def main():
    print("Press q to exit...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        cap.open()
        if not cap.isOpened():
            print("Can't find camera...")
            exit()

    while(True):
        ret,frame = cap.read()
        cv2.imshow('Camera Test', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
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
