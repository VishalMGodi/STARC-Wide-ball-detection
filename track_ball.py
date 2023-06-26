import cv2 as cv
import numpy as np

# Open the video
cap = cv.VideoCapture(r'SampleDatasetSTARC/9_Kan_C.mp4')

object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

while True:

	# Extract frames one after the other
	ret, frame = cap.read()

	# If there are no more frames, break the loop
	if not ret:
		break

	# Create the mask
	mask = object_detector.apply(frame)

	# Find the contours
	contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	for cnt in contours:

		# Calculate the area and eliminate small contours
		area = cv.contourArea(cnt)
		if (area < 100):
			continue

		# Calculate the perimeter of the contour
		perimeter = cv.arcLength(cnt, True)

		# Calculate the circularity of the contour
		circularity = 4 * np.pi * (area / (perimeter * perimeter))

		# Filter contours based on circularity
		if circularity < 0.5:
			continue

		# Draw the contours
		cv.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

	# Show the video
	cv.imshow('frame', frame)

	# Stop if 'q' key is pressed
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

# Release the video capture and close all windows
cap.release()