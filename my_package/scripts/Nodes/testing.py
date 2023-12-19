import cv2
import numpy as np

# Load the video file
img = cv2.imread("/home/revanth/Tennistron/tennyson_ws/src/my_package/data/top_view.jpg")

print(img.shape)
cv2.imshow("Image",img)

key = cv2.waitKey(0)
cv2.destroyAllWindows()
