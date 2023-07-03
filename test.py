# import mediapipe as mp
# from vpython import *
# import cv2

# # Create a VPython scene and a 3D object to represent the detected pose
# scene = canvas(title='Pose Detection', width=800, height=600)
# sphereObj = sphere(radius=0.05, color=color.red)

# # Create a mediapipe drawing object for drawing landmarks
# mp_drawing = mp.solutions.drawing_utils
# mp_holistic = mp.solutions.holistic

# # Initialize the MediaPipe Pose model
# mp_pose = mp.solutions.pose.Pose()

# # Start the webcam feed
# cap = cv2.VideoCapture(0)


# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = mp_pose.process(frame_rgb)

#     if results.pose_landmarks:
#         landmarks = results.pose_landmarks.landmark
#         mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
#         # Get the position of a specific landmark (e.g., nose)
#         # and update the pose object's position in VPython
#         sphereObj.pos = vector(landmarks[mp.solutions.pose.PoseLandmark.NOSE].x,
#                                  landmarks[mp.solutions.pose.PoseLandmark.NOSE].y,
#                                  0)
#     cv2.namedWindow("MediaPipe Pose", cv2.WINDOW_NORMAL)
#     cv2.resizeWindow("MediaPipe Pose", 800,600)
#     cv2.imshow('MediaPipe Pose', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         sphereObj.pos = vector(0,0,0)
#         break

# mp_pose.close()
# cap.release()
# cv2.destroyAllWindows()
# quit()

# Dataset/Alldone/9_Kan_C.mp4

# import cv2 as cv
# import numpy as np

# # Open the video
# cap = cv.VideoCapture(r'Dataset/Alldone/9_Kan_C.mp4')

# object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

# while True:

# 	# Extract frames one after the other
# 	ret, frame = cap.read()

# 	# If there are no more frames, break the loop
# 	if not ret:
# 		break

# 	# Create the mask
# 	mask = object_detector.apply(frame)

# 	# Find the contours
# 	contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# 	for cnt in contours:

# 		# Calculate the area and eliminate small contours
# 		area = cv.contourArea(cnt)
# 		if (area < 100):
# 			continue

# 		# Calculate the perimeter of the contour
# 		perimeter = cv.arcLength(cnt, True)

# 		# Calculate the circularity of the contour
# 		circularity = 4 * np.pi * (area / (perimeter * perimeter))

# 		# Filter contours based on circularity
# 		if circularity < 0.4:
# 			continue

# 		# Draw the contours
# 		cv.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

# 	# Show the video
# 	cv.imshow('frame', frame)

# 	# Stop if 'q' key is pressed
# 	if cv.waitKey(1) & 0xFF == ord('q'):
# 		break

# # Release the video capture and close all windows
# cap.release()



# https://www.youtube.com/watch?v=RaCwLrKuS1w

# import cv2
# import numpy as np

# videoCapture = cv2.VideoCapture(r'Dataset/Alldone/9_Kan_C.mp4')
# prevCircle = None
# dist = lambda x1,y1,x2,y2: (x1-x2)**2*(y1-y2)**2

# while True:
# 	ret, frame = videoCapture.read()
# 	if not ret: 
# 		break

# 	grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	blurFrame = cv2.GaussianBlur(grayFrame, (25,25), 0)
# 	circles = cv2.HoughCircles(blurFrame,cv2.HOUGH_GRADIENT,1,100,param1=10,param2=2,minRadius=0,maxRadius=30)
# 	# cv2.imshow("test",blurFrame)
# 	# input()
# 	if circles is not None:
# 		circles = np.uint16(np.around(circles))
# 		chosen = None
# 		for i in circles[0,:]:
# 			if chosen is None:
# 				chosen = i
# 			if prevCircle is not None:
# 				if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1]) <= dist(i[0],i[1],prevCircle[0],prevCircle[1]):
# 					chosen  = i
# 		cv2.circle(frame,(chosen[0],chosen[1]), 1, (0,100,100), 3)
# 		cv2.circle(frame,(chosen[0],chosen[1]), chosen[2], (255,0,255), 3)
# 		prevCircle = chosen
# 	cv2.imshow("circles", frame)

# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 		break

# videoCapture.release()
# cv2.destroyAllWindows()


###############

import cv2
img = cv2.imread(r'Dataset\batsmanMovementDataset\_DSC3114.JPG') # load a dummy image
while(1):
    cv2.imshow('img',img)
    k = cv2.waitKey(33)
    if k==27:    # Esc key to stop
        break
    elif k==-1:  # normally -1 returned,so don't print it
        continue
    else:
        print(k) # else print its value