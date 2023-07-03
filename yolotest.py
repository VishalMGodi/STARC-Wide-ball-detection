import cv2 as cv
import numpy as np

# Load the YOLOv3 model
net = cv.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# Load the class labels
with open('coco.names', 'r') as f:
    classes = f.read().splitlines()

# Set the confidence threshold for detection
conf_threshold = 0.5

# Set the non-maximum suppression threshold
nms_threshold = 0.4

# Open the video
cap = cv.VideoCapture(r'Sample Dataset STARC\9_Kan_C.mp4')

while True:
    # Extract frames one after the other
    ret, frame = cap.read()

    # If there are no more frames, break the loop
    if not ret:
        break

    # Create a blob from the frame
    blob = cv.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)

    # Set the input for the network
    net.setInput(blob)

    # Perform forward pass and get the output layer names
    output_layers_names = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers_names)

    # Initialize lists for bounding boxes, confidences, and class IDs
    boxes = []
    confidences = []
    class_ids = []

    # Iterate over each output layer
    for output in layer_outputs:
        # Iterate over each detection
        for detection in output:
            # Get the class scores and class ID
            scores = detection[5:]
            class_id = np.argmax(scores)

            # Filter detections based on confidence threshold
            confidence = scores[class_id]
            if confidence > conf_threshold:
                # Scale the bounding box coordinates to the original frame size
                width = frame.shape[1]
                height = frame.shape[0]
                x, y, w, h = detection[0:4] * np.array([width, height, width, height])

                # Calculate the top-left corner coordinates
                x = int(x - w/2)
                y = int(y - h/2)

                # Store the bounding box coordinates, confidence, and class ID
                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Set the class label for cricket ball
    cricket_ball_class_id = classes.index('sports ball')

    # Apply non-maximum suppression to eliminate redundant overlapping boxes
    if len(boxes) > 0:
        indices = cv.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        if len(indices) > 0:
            # Iterate over the filtered detections
            for i in indices.flatten():
                class_id = class_ids[i]
                
                # Filter only the cricket ball detections
                if class_id == cricket_ball_class_id:
                    x, y, w, h = boxes[i]
                    label = classes[class_id]
                    confidence = confidences[i]

                    # Draw the bounding box
                    cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    # Draw the label and confidence
                    text = f'{label}: {confidence:.2f}'
                    cv.putText(frame, text, (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


    # Show the video with detected objects
    cv.imshow('frame', frame)

    # Stop if 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv.destroyAllWindows()


# import cv2 as cv
# import numpy as np

# # Open the video
# cap = cv.VideoCapture(r'Sample Dataset STARC\9_Kan_C.mp4')

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
# 		if circularity < 0.3:
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