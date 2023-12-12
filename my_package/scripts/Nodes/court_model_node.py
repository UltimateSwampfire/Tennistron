#!/usr/bin/env python3

# import necessary libraries 
import cv2 
import numpy as np
import rospy
from std_msgs.msg import String
 


top_view = cv2.imread("/home/revanth/Tennistron/tennyson_ws/src/my_package/data/top_view.jpg")

pts1 = np.float32([[241, 87], [714, 86],
	               [59, 476], [999, 464]])
pts2 = np.float32([[85, 95], [274,95],
	               [85, 502], [274, 502]])
	               
	             	
# Apply Perspective Transform Algorithm
matrix = cv2.getPerspectiveTransform(pts1, pts2)

x = 0
y = 0


shot_array = [["Left Lob","Left Flat Volley", "Left Topspin", "Left Drop and Slice"],
["Right Lob","Right Flat Volley", "Right Topspin", "Right Drop and Slice"]]


def shot_selector(x_t,y_t):

	side = []
	shot = ""
	
	if x_t <= 180 :		
		side = shot_array[0]
	else:
		side = shot_array[1]
		
	#Left shots
	if y_t <=350:
		shot = side[0]
	elif y_t > 350 and y_t <= 400:
		shot = side[1]
	elif y_t > 400 and y_t <= 450:
		shot = side[2]
	elif y_t > 450:
		shot = side[3]
	else:
		shot = "Whip and dip"
	return shot


def player_position_callback(data):
	
	global x, y
	msg = data.data
	x , y = [int(value) for value in msg.split(",")]
	#source_point = np.array([[x, y]], dtype=np.float32)
	#rospy.loginfo(rospy.get_caller_id() + 'I heard %s', msg)
	
	
	

if __name__ == "__main__":

	
	try:
		#Updates x_t and y_t
		rospy.init_node("Model", anonymous = True)
		rospy.Subscriber("player_position", String, player_position_callback)
		
		
		while True:
			model = top_view.copy()

			source_point = np.array([x, y], dtype=np.float32)

			transformed_point = cv2.perspectiveTransform(np.array([[source_point]],
			dtype=np.float32), matrix)

			transformed_point = tuple(map(int, transformed_point[0][0]))
			
			x_t, y_t = transformed_point
			print("Source : ",source_point, "Transformed : " ,transformed_point)
			cv2.circle(model, (int(x_t),int(y_t)),10,(0,255,255),-1)
			
			shot = shot_selector(x_t,y_t)
			print(shot)
			font = cv2.FONT_HERSHEY_SIMPLEX
			color = (0,0,255)
			cv2.putText(model, f"Shot Selected : {shot}",(10,30),font,
			0.6,(255,100,0),2)
			cv2.imshow("Court Model", model) # Transformed Capture

			if cv2.waitKey(int(1000/30)) == ord('q'):
				break

		cv2.destroyAllWindows()
	except rospy.ROSInterruptException:
		pass
