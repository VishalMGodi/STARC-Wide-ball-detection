# import cv2
# import cvzone
# from cvzone.FaceMeshModule import FaceMeshDetector

# cap = cv2.VideoCapture(0)
# detector = FaceMeshDetector(maxFaces=1)

# while True:
#     success, frame = cap.read()
#     frame, faces = detector.findFaceMesh(frame, draw=False)

#     if faces:

#         face = faces[0]
#         pointLeft = face[145]
#         pointRight = face[374]
#         # Drawing
#         # cv2.line(frame, pointLeft, pointRight, (0, 200, 0), 3)
#         # cv2.circle(frame, pointLeft, 5, (255, 0, 255), cv2.FILLED)
#         # cv2.circle(frame, pointRight, 5, (255, 0, 255), cv2.FILLED)
#         w, _ = detector.findDistance(pointLeft, pointRight)
#         W = 6.3

#         # # Finding the Focal Length
#         d = 50
#         f = (w*d)/W
#         print(f"f: {f}")

#         # Finding distance
#         # f = 840
#         # d = (W * f) / w
#         # # print(f"d: {d}")
#         # print(f'\rD: {round(d,2)}', end='', flush=True)

#         cvzone.putTextRect(frame, f'Depth: {int(d)}cm',
#                            (face[10][0] - 100, face[10][1] - 50),
#                            scale=2)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#     cv2.imshow("Image", frame)
#     cv2.waitKey(1)

import cv2
import mediapipe as mp
import math

# Initialize the MediaPipe Holistic model
mp_holistic = mp.solutions.holistic

# Start the webcam feed
cap = cv2.VideoCapture(0)

# Object dimension for reference (e.g., height of a person)
object_height = 1.7  # meters

# Create a MediaPipe Holistic object
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Use the MediaPipe Holistic model to detect landmarks and calculate the depth
        results = holistic.process(frame_rgb)
        landmarks = results.pose_landmarks

        if landmarks is not None:
            # Get the depth value of a specific landmark (e.g., nose)
            neck_landmark = landmarks.landmark[mp_holistic.PoseLandmark.NOSE]
            neck_depth = neck_landmark.z

            # Calculate the distance using a reference object's height
            distance_cm = object_height * (1 / neck_depth) * 100

            # Display the distance on the frame
            cv2.putText(frame, f"Distance: {distance_cm:.2f} cm", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
