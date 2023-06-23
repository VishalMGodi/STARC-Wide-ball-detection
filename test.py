import cv2
import numpy as np
import mediapipe as mp

# Convert color range to HSV
def convert_color_range(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return hsv

# Detect objects based on color range
def detect_objects(frame, lower_color, upper_color):
    mask = cv2.inRange(frame, lower_color, upper_color)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_objects = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # adjust the area threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            detected_objects.append((x, y, w, h))
    return detected_objects

# Load video
# video = cv2.VideoCapture(r'Sample Dataset STARC\18_Kan_C.mp4')
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
# cap = cv2.VideoCapture(r'Sample Dataset STARC\TestSubject2_Edited.mp4')
cap = cv2.VideoCapture(r'Sample Dataset STARC\9_Kan_C.mp4')

# Define color range for detection
lower_green = np.array([0, 0, 200])
upper_green = np.array([179, 30, 255])

# Read the video frames
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # FACE
        # mp_drawing.draw_landmarks(frame, results.face_landmarks, mp.solutions.face_mesh.FACEMESH_CONTOURS)
        # RIGHT HAND
        # mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        # LEFT HAND
        # mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        # POSE
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        
       # Convert color range to HSV
        hsv = convert_color_range(frame)

        # Detect objects
        detected_objects = detect_objects(hsv, lower_green, upper_green)

        # Visualize the results
        for (x, y, w, h) in detected_objects:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the frame with detections
        cv2.imshow('Color Detection', frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
cv2.calibrateCamera