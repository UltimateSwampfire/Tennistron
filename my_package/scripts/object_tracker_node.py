#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
#from select_roi import ROISelector

class ObjectTrackerNode:
    def __init__(self):
        rospy.init_node('object_tracker')
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.image_callback)
        self.tracker = None
        self.tracking = False

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            (X,Y) = cv_image.shape[0], cv_image.shape[1]
        except CvBridgeError as e:
            print(e)
            return
            
          

        if self.tracking:
            success, new_box = self.tracker.update(cv_image)
            if success:
                (x, y, w, h) = (int(new_box[0]), int(new_box[1]), int(new_box[2]),int(new_box[3]))
                cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                center = "( %i , %i)" %(x,y)
                cv2.putText(cv_image, "Success" if success else "Failure", (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
                cv2.putText(cv_image, center, (int(x+w/2),int(y+h/2)),
                cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)


        cv2.imshow("Object Tracking", cv_image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            self.tracking = not self.tracking
            if self.tracking:
                (x, y, w, h) = cv2.selectROI("Object Tracking",cv_image, True, False)
                self.tracker = cv2.TrackerKCF_create()
                self.tracker.init(cv_image, (x, y, w, h))

        elif key == ord("q"):
            rospy.signal_shutdown("User quit")
            cv2.destroyAllWindows()


if __name__ == '__main__':
    tracker_node = ObjectTrackerNode()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()


