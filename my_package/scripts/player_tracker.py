# import the necessary packages
import numpy as np
import cv2
import imutils


def getFirstFrame(vidcap):
	success, image = vidcap.read()
	if success:
		return image

vs = cv2.VideoCapture("/home/revanth/Tennistron/tennyson_ws/src/my_package/data/cropped.mov")
first_frame = (getFirstFrame(vs))
bounding_box = ((356, 334),(481,334),(356, 496),(481,496))
initBB = (356,334,120,160)

tracker = cv2.TrackerKCF_create()
tracker.init(first_frame, initBB)
fps = vs.get(cv2.CAP_PROP_FPS)


while True:
	
	frame = vs.read()[1]
	if frame is None:
		break
	success, new_box = tracker.update(frame)
	if success:
		(x, y, w, h) = (int(new_box[0]), int(new_box[1]), int(new_box[2]),int(new_box[3]))
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		center = "( %i , %i)" %(x,y)
		
		player_coords = (int(x+w/2), int(y+h))
		
		font = cv2.FONT_HERSHEY_SIMPLEX
		color = (0,0,255)
		cv2.putText(frame, f"({player_coords[0]},{player_coords[1]})",player_coords,font,
		0.6,color,2)
		cv2.putText(frame, "Success" if success else "Failure", (x,y),
		font,0.6,color,2)
		cv2.putText(frame, center, (int(x+w/2),int(y+h/2)),
		font,0.6,color,2)
			
		
	cv2.imshow("Frame",frame)
	
	key = cv2.waitKey(int(1000/fps)) & 0xFF
	
	if key == ord('q'):
		vs.release()
cv2.destroyAllWindows()

