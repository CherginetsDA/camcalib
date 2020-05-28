#!/usr/bin/env python
import argparse
import cv2
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

bridge = CvBridge()
cv_image = cv2.imread('../image/cat.jpg')

def callback(image_message):
    global cv_image
    cv_image = bridge.imgmsg_to_cv2(image_message, desired_encoding='passthrough')

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/usb_cam/image_raw", Image, callback)
    while(True):
        cv2.imshow('Camera Test', cv_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    print("Done.")

if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        exit()
