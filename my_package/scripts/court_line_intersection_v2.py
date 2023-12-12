import cv2
import numpy as np
import opencv_wrapper as cvw
    
###################################################################################

# Load the input image
image = cv2.imread('/home/revanth/Tennistron/tennyson_ws/src/my_package/data/2.png')  # Replace with the path to your image

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Define the lower and upper bounds for the color of the tennis court lines
lower_bound = np.array([200, 200, 200], dtype=np.uint8)  # Adjust as needed
upper_bound = np.array([255, 255, 255], dtype=np.uint8)  # Adjust as needed


# Apply Bilateral blur to the grayscale image to reduce noise
gray_blurred = cv2.bilateralFilter(gray,30,25,75)

# Create a binary mask to isolate the tennis court lines
mask = cv2.inRange(gray_blurred, 200, 255)

##############################################################

#dst = cv2.Canny(mask, 50, 200, None, 3)
dst = mask

linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 5)


lines_image = np.zeros(image.shape,dtype = "uint8")

if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        cv2.line(lines_image, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv2.LINE_AA)
        
        
###################################################################
# Start my code
lines_gray = cv2.cvtColor(lines_image, cv2.COLOR_BGR2GRAY)
corners = cv2.cornerHarris(lines_gray, 9, 3, 0.01)
corners = cvw.normalize(corners).astype(np.uint8)

thresh = cvw.threshold_otsu(corners)
dilated = cvw.dilate(thresh, 3)

contours = cvw.find_external_contours(dilated)

for contour in contours:
    cvw.circle(lines_image, contour.center, 6, cvw.Color.GREEN, -1)
    cvw.circle(image, contour.center, 6, cvw.Color.GREEN, -1)

###################################################################


# Display the original image with the detected tennis court corners


# Show results
cv2.imshow("Source", image)
#cv2.imshow("gray blurred", gray_blurred)
cv2.imshow("Lines Only", lines_image)
cv2.imshow('MASK', mask)
#cv2.imshow('Tennis Court Corners', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

