import numpy as np
import cv2

pts1 = np.float32([[241, 87], [714, 86],
	               [59, 476], [999, 464]])
pts2 = np.float32([[85, 95], [274,95],
	               [85, 502], [274, 502]])
	               
	             	
# Apply Perspective Transform Algorithm
matrix = cv2.getPerspectiveTransform(pts1, pts2)

image = cv2.imread("/home/revanth/Tennistron/tennyson_ws/src/my_package/data/0.png")

source_point = np.array([100, 200], dtype=np.float32)

transformed_point = cv2.perspectiveTransform(np.array([[source_point]],
dtype=np.float32), matrix)

print(transformed_point)



