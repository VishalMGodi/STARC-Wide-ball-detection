import cv2 as cv
import numpy as np

# Video file path
video_path = '/Users/varun/Desktop/Projects/STARC/STARC-Wide-ball-detection/Dataset/New_6_MainView.mp4'
cap = cv.VideoCapture(video_path)
cap.set(3, 1920)
cap.set(4, 1080)

# Create the background subtractor object
object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

#Make a set of coordinates
ball_coords = []
final_pos = None

def process_frame(frame):

    # Create the mask
    mask = object_detector.apply(frame)

    # Find the contours
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:

        # Calculate the area and eliminate small contours
        area = cv.contourArea(cnt)

        if area < 400:
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

        # pixel color checks
        if (frame[cnt[0][0][1]][cnt[0][0][0]][2] < 115) or (frame[cnt[0][0][1]][cnt[0][0][0]][2] > 135):
            continue

        # if (frame[cnt[0][0][1]][cnt[0][0][0]][1] < 75) or (frame[cnt[0][0][1]][cnt[0][0][0]][1] > 90):
        #     continue

        if (frame[cnt[0][0][1]][cnt[0][0][0]][0] < 100) or (frame[cnt[0][0][1]][cnt[0][0][0]][0] > 120):
            continue

        # Add the coordinates of the contour
        ball_coords.append((cv.boundingRect(cnt), "Main"))

    cv.imshow('Frame', frame)


while True:
    ret, frame = cap.read()
    if frame is None:
        break

    # Resize the frame
    frame = cv.resize(frame, (1920, 1080), fx=0, fy=0, interpolation=cv.INTER_CUBIC) 

    process_frame(frame)
    if True:

        # Draw boxes for all the coordinates      
        for i, coord in enumerate(ball_coords):
            if(coord[1] == "Main"):
                cv.rectangle(frame, (coord[0][0], coord[0][1]), (coord[0][0]+coord[0][2], coord[0][1]+coord[0][3]), (0, 0, 255))
            elif(coord[1] == "Buffer"):
                cv.rectangle(frame, (coord[0][0], coord[0][1]), (coord[0][0]+coord[0][2], coord[0][1]+coord[0][3]), (255, 255, 0))

        cv.imshow('Frame', frame)

        # Move frames when 'p' is pressed
        while True:
            if (cv.waitKey(0) & 0xFF == ord('p')):
                break

    if (cv.waitKey(1) & 0xFF == ord('q')):
        break

final_pos = ball_coords[-1]

print(f"TRAJECTORY: {ball_coords}\nFINAL POSITION: {final_pos}")

# Release the video capture object and close any open windows
cap.release()
cv.destroyAllWindows()
