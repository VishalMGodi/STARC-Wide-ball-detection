import cv2
import numpy as np

# Load the image
image = cv2.imread('./Dataset/Alldone/Sample_Pic_Batsman.png')  # Replace 'image.jpg' with the path to your image file

# Convert the image to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the lower and upper color thresholds to remove
lower_color = np.array([40, 40, 40])  # Lower color threshold (in HSV)
upper_color = np.array([0, 255, 0])  # Upper color threshold (in HSV)
# lower_color = np.array([60, 0.157, 0.586])  # Lower color threshold (in HSV)
# upper_color = np.array([65.29, 0.23, 0.565])  # Upper color threshold (in HSV)

# Create a mask based on the color thresholds
mask = cv2.inRange(hsv_image, lower_color, upper_color)

# Apply the mask to the original image
result = cv2.bitwise_and(image, image, mask=mask)

# Display the original image and the resulting image
cv2.imshow('Original Image', image)
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
