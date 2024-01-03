# import necessary libraries 
import cv2 
import numpy as np 
 


vs = cv2.VideoCapture("/home/revanth/Tennistron/tennyson_ws/src/my_package/data/cropped.mov")
top_view = cv2.imread("/home/revanth/Tennistron/tennyson_ws/src/my_package/data/top_view.jpg")



while True:
     
    frame = vs.read()[1]
 
    # Locate points of the documents
    # or object which you want to transform

    pts1 = np.float32([[241, 87], [714, 86],
                       [59, 476], [999, 464]])
    pts2 = np.float32([[85, 95], [274,95],
                       [85, 502], [274, 502]])
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    
    mask = np.zeros(top_view.shape[:2], dtype = np.uint8)
    
    top_left = np.int32(pts2[0])
    bottom_right = np.int32(pts2[3])
    mask[ top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]] = 255

    print(matrix)
    result = cv2.warpPerspective(frame, matrix, (360, 599))
    result = cv2.bitwise_and(result, result, mask = mask)
     
    # Wrap the transformed image
    cv2.imshow('frame', frame) # Initial Capture
    cv2.imshow('frame1', result) # Transformed Capture
 
    if cv2.waitKey(24) == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
