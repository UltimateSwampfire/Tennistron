#!/usr/bin/env python3

import rospy
import cv2
from std_msgs.msg import Header
from my_package.msg import ImgCords


#added an aribitrary comment 
# Define a list to store the selected points


def corner_selector_node():

	rospy.init_node("corner_selector")
	
	#Order : Top Left, Top Right, Bottom Left, Bottom Right
	x_points = []
	y_points = []

	#------------GETTING USER DATA--------------#
	
	# Mouse callback function
	def select_point(event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONDOWN:
		    # Append the selected point to the list
		    x_points.append(x)
		    y_points.append(y)
		    # Display a circle at the selected point
		    cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

	# Load your image here
	image = cv2.imread('/home/revanth/Tennistron/tennyson_ws/src/my_package/data/top_view.jpg')

	# Create a window for displaying the image
	cv2.namedWindow('Select Points')
	# Set the mouse callback function
	cv2.setMouseCallback('Select Points', select_point)

	while True:
		cv2.imshow('Select Points', image)
		key = cv2.waitKey(1) & 0xFF
		# If 'q' is pressed, break the loop
		if key == ord('q'):
		    break
	
	
	pub = rospy.Publisher("corner_points",ImgCords,queue_size = 10)
	
	msg = ImgCords()
	msg.x = x_points
	msg.y = y_points

	pub.publish(msg)
	
	rospy.signal_shutdown("Data Published. Exiting Corner Selector.")
	rospy.loginfo(list(zip(x_points,y_points)))

	rospy.spin()
	

if __name__ == "__main__":
	corner_selector_node()

#rospy.loginfo(f"Four corner points are {x_points} and {y_points}")
# Print the selected points
#print("Selected Points:", selected_points)

