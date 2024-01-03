#!/usr/bin/env python3

# import necessary libraries 
import cv2 
import numpy as np
import rospy
from std_msgs.msg import String
 


vs = cv2.VideoCapture("/home/revanth/Tennistron/tennyson_ws/src/my_package/data/cropped.mov")
top_view = cv2.imread("/home/revanth/Tennistron/tennyson_ws/src/my_package/data/top_view.jpg")

pts1 = np.float32([[241, 87], [714, 86],
	               [59, 476], [999, 464]])
pts2 = np.float32([[85, 95], [274,95],
	               [85, 502], [274, 502]])
	               
	             	
# Apply Perspective Transform Algorithm
matrix = cv2.getPerspectiveTransform(pts1, pts2)

x = 0
y = 0


def player_position_callback(data):
	
	global x, y
	msg = data.data
	x , y = [int(value) for value in msg.split(",")]
	#source_point = np.array([[x, y]], dtype=np.float32)
	#rospy.loginfo(rospy.get_caller_id() + 'I heard %s', msg)
	
	
	

if __name__ == "__main__":

	
	try:
		#Updates x_t and y_t
		rospy.init_node("BEV_transformer", anonymous = True)
		rospy.Subscriber("player_position", String, player_position_callback)
		
		
		while True:
			frame = vs.read()[1]
			model = top_view.copy()

			# Locate points of the documents
			# or object which you want to transform

			mask = np.zeros(top_view.shape[:2], dtype = np.uint8)

			top_left = np.int32(pts2[0])
			bottom_right = np.int32(pts2[3])
			mask[ top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]] = 255


			source_point = np.array([x, y], dtype=np.float32)
			
			transformed_point = cv2.perspectiveTransform(np.array([[source_point]],
			dtype=np.float32), matrix)

			transformed_point = tuple(map(int, transformed_point[0][0]))
			
			x_t, y_t = transformed_point
			print("Source : ",source_point, "Transformed : " ,transformed_point)

			# Draw a dot on the transformed image

			result = cv2.warpPerspective(frame, matrix, (360, 599))
			result = cv2.bitwise_and(result, result, mask = mask)

			cv2.circle(result, (int(x_t),int(y_t)),10,(0,69,255),-1)
			cv2.circle(model, (int(x_t),int(y_t)),10,(0,255,255),-1)
			 
			# Wrap the transformed image
			#cv2.imshow('frame', frame) # Initial Capture
			cv2.imshow("Bird's Eye View", result) # Transformed Capture
			#cv2.imshow("Court Model", model) # Transformed Capture

			if cv2.waitKey(int(1000/30)) == ord('q'):
				vs.release()
				break
				
		cv2.destroyAllWindows()
		
	except rospy.ROSInterruptException:
		pass
