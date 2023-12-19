#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import imutils

def image_callback(msg):
    try:
        bridge = CvBridge()
        frame = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
    except CvBridgeError as e:
        rospy.logerr(e)
        
    cv2.imshow("Modified Image", frame)
    cv2.waitKey(3)
    
    
def image_subscriber():
    rospy.init_node("image_subscriber", anonymous=True)
    rospy.Subscriber("/usb_cam/image_raw", Image, image_callback)
    rospy.spin()

if __name__ == "__main__":
    image_subscriber()
    
   
   

