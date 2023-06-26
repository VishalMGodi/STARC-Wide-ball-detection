import mediapipe as mp
import cv2
from vpython import *


scene = canvas(title='Pose Mapping', width=800, height=600)
box(pos=vector(0, 0, 0), size=vector(2, 2, 2), color=color.red)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)


cap = cv2.VideoCapture(0)  # Adjust the parameter if using a different camera

while True:
    ret, frame = cap.read()
    
    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)
    
    # Process the frame with Mediapipe pose detection
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    
    # Map the pose on the VPython output
    if results.pose_landmarks is not None:
        # Clear previous VPython objects
        scene.delete()
        
        # Draw the box
        box(pos=vector(0, 0, 0), size=vector(2, 2, 2), color=color.red)
        
        # Get the pose landmarks
        landmarks = results.pose_landmarks.landmark
        
        # Map each landmark to VPython coordinates and draw spheres
        for landmark in landmarks:
            x = landmark.x * 4 - 2  # Adjust the scaling and offset as per your requirements
            y = landmark.y * 4 - 2
            z = -landmark.z * 4  # Negative value to bring landmarks in front of the box
            
            sphere(pos=vector(x, y, z), radius=0.05, color=color.green)
    
    # Display the frame
    cv2.imshow('Pose Mapping', frame)
    
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
