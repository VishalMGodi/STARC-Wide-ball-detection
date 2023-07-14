import cv2 as cv
import numpy as np

# Open the video
cap = cv.VideoCapture(r'/Users/varun/Downloads/Dataset/New_5_BatView.mp4')
cap.set(3, 1280)
cap.set(4, 720)

object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

ball_coords = []

while True:

	i = 0

	# Extract frames one after the other
	ret, frame = cap.read()

	# If there are no more frames, break the loop
	if not ret:
		break

	# Resize frame
	frame = cv.resize(frame, (0, 0), None, 0.5, 0.5)

	# Blur the frame
	frame = cv.GaussianBlur(frame, (11, 11), 0)

	# Create the mask
	mask = object_detector.apply(frame)

	# Find the contours
	contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	for cnt in contours:

		# Calculate the area and eliminate small contours
		area = cv.contourArea(cnt)

		if ((area < 40) or (area > 80)):
			continue

		# Calculate the perimeter of the contour
		perimeter = cv.arcLength(cnt, True)

		if perimeter == 0:
			continue

		# Calculate the circularity of the contour
		circularity = 4 * np.pi * (area / (perimeter * perimeter))

		# Filter contours based on circularity
		if circularity < 0.5:
			continue

		# If cnt pixel color is not red, continue
		if (frame[cnt[0][0][1]][cnt[0][0][0]][2] < 95) or (frame[cnt[0][0][1]][cnt[0][0][0]][2] > 106):
			continue

		# Draw the contours
		# cv.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

		# Find the bounding box coordinates
		x, y, w, h = cv.boundingRect(cnt)

		ball_coords.append((x, y, w, h))

		for coords in ball_coords:
			# Draw a filled rectangle with a number inside
			# cv.rectangle(frame, (coords[0], coords[1]), (coords[0] + coords[2], coords[1] + coords[3]), (0, 0, 255),
			#              cv.FILLED)
			cv.putText(frame, str(i), (coords[0]+10, coords[1]+10), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
			i += 1
			print(i, frame[cnt[0][0][1]][cnt[0][0][0]])	

		# print(i, area)

		while True:
			if cv.waitKey(1) & 0xFF == ord('q'):
				break

		# print(ball_coords)

	# Show the video
	cv.imshow('frame', frame)

	# Stop if 'q' key is pressed
	if cv.waitKey(1) & 0xFF == ord('p'):
		break

# Release the video capture and close all windows
cap.release()