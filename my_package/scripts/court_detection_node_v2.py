# import the necessary packages
import numpy as np
import cv2
#import opencv_wrapper as cvw
import imutils
import time

# import  poly_point_isect as bot

# construct the argument parse and parse the arguments
# construct the argument parse and parse the arguments

# load the image
vs = cv2.VideoCapture("/home/revanth/Tennistron/tennyson_ws/src/my_package/data/cropped.mov")


# define the list of Color boundaries
lower, upper = np.array([180, 180, 100]), np.array([255, 255, 255])

mask_list = []
points_list = []

frame_count = 0
start_time = time.time()


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
	mask = cv2.inRange(gray_blurred, 160, 255)
	mask = cv2.dilate(mask,(7,7),None)
	
	
	############ Long exposure of Line Detection for less noise######
	
	mask_list.append(mask)
	
	
	if len(mask_list) == 10:
		mask_list.pop(0)
	summed = sum(mask_list)
	summed = cv2.dilate(summed,(7,7),None)
	#################################################################

	##Lines Stuff##
	
	lines = cv2.HoughLinesP(summed, 1, np.pi/180, 50, None, 50, 5)
	lines_image = np.zeros(frame.shape, dtype = frame.dtype)
	
	if lines is not None:
		for i in range(0, len(lines)):
		    l = lines[i][0]
		    cv2.line(lines_image, (l[0], l[1]), (l[2], l[3]), (0,0,255), 2, cv2.LINE_AA)
		    cv2.line(frame, (l[0], l[1]), (l[2], l[3]), (0,0,255), 2, cv2.LINE_AA)
		    

	lines_image_gray = cv2.cvtColor(lines_image, cv2.COLOR_BGR2GRAY)

	#################################################################
	
	corners = cv2.goodFeaturesToTrack(summed, maxCorners = 50, qualityLevel = 0.1,
	minDistance = 150, blockSize = 3, useHarrisDetector = False)
	
	
	for corner in corners:
		x,y = int(corner[0][0]), int(corner[0][1])
		
		print(x,y)
		cv2.circle(frame, (x,y), 8, (0,255,0), -1)
		cv2.circle(lines_image, (x,y), 8, (0,255,0), -1)
		
	#Update points_list
	points_list.append(corners)


	frame_count = frame_count + 1
	end_time = time.time()
	
	fps = round(frame_count/(end_time - start_time),1)
	cv2.putText(frame, f"FPS : {fps}", (10,30),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2)
	


	#cv2.imshow("Mask", mask)
	cv2.imshow("Frame", frame)
	cv2.imshow("Video", lines_image_gray)
	cv2.imshow("Mask Exposure",summed)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		vs.release()
		
cv2.destroyAllWindows()

