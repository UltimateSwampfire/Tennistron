# import the necessary packages
import numpy as np
import cv2
import opencv_wrapper as cvw
import imutils

# import  poly_point_isect as bot

# construct the argument parse and parse the arguments
# construct the argument parse and parse the arguments

# load the image
vs = cv2.VideoCapture("/home/revanth/Tennistron/tennyson_ws/src/my_package/data/cropped.mov")


# define the list of Color boundaries
lower, upper = np.array([180, 180, 100]), np.array([255, 255, 255])

while True:
	
	#Read the current Frame
	frame = vs.read()[1]	
	fps = int(vs.get(cv2.CAP_PROP_FPS))
	if frame is None:
		break
	
	#Frame Image Processing
	
	#frame = imutils.resize(frame, width = 800)
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray_blurred = cv2.bilateralFilter(gray_frame, 30, 25, 75)
	mask = cv2.inRange(gray_blurred, 200, 255)
	
	
	
	corners = cv2.goodFeaturesToTrack(mask, maxCorners = 100, qualityLevel = 0.2,
	minDistance = 50, blockSize = 3, useHarrisDetector = False)
	
	

	for corner in corners:
		x,y = int(corner[0][0]), int(corner[0][1])
		
		print(x,y)
		cv2.circle(frame, (x,y), 8, (0,255,0), -1)


	cv2.imshow("Mask", mask)
	cv2.imshow("Video", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		vs.release()
		
cv2.destroyAllWindows()

