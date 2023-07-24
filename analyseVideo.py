import cv2 as cv
import numpy as np

# Video file path
video_path = '/Users/varun/Downloads/Dataset/New_2_BatView.mp4'
cap = cv.VideoCapture(video_path)

# Create the background subtractor object
object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

#Make a set of coordinates
ball_coords = set({})

# Flag to check if ball is detected
ball_detected = False

def process_frame(frame):

    global ball_detected    

    # Create the mask
    mask = object_detector.apply(frame)

    # Find the contours
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:

        i = 0

        # Calculate the area and eliminate small contours
        area = cv.contourArea(cnt)

        # Draw the main rectangle within which the objects need to be detected
        xM = int(frame.shape[1]/2.25)
        yM = int(frame.shape[0]/2)
        x2M = int(frame.shape[1]/3.0)
        y2M = int(frame.shape[0]/1.2)
        cv.rectangle(frame, (xM, yM), (x2M, y2M), (255, 0, 0), 5)

        # Draw a buffer rectangle within which the objects need to be detected if its not detected withing the main rectangle
        xB = int(frame.shape[1]/3.75)
        yB = int(frame.shape[0]/2)
        x2B = int(frame.shape[1]/2.25)
        y2B = int(frame.shape[0]/1.2)

        # cv.circle(frame, (x, y), 15, (255, 0, 0), cv.FILLED)
        # cv.circle(frame, (x2, y2), 15, (0, 255, 0), cv.FILLED)

        cv.rectangle(frame, (xB, yB), (x2B, y2B), (0, 0, 255))

        if area < 70:
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

        # check if the contour is within the main rectangle
        if (cnt[0][0][0] > xM) and (cnt[0][0][0] < x2M) and (cnt[0][0][1] > yM) and (cnt[0][0][1] < y2M):
            ball_coords.add((cv.boundingRect(cnt), "Main"))
            # Draw the contours
            cv.drawContours(frame, [cnt], -1, (0, 255, 255), 2)
            ball_detected = True
            break

        # Check if its within the buffer rectangle
        elif (cnt[0][0][0] > xB) and (cnt[0][0][0] < x2B) and (cnt[0][0][1] > yB) and (cnt[0][0][1] < y2B):
            ball_coords.add((cv.boundingRect(cnt), "Buffer"))
            # Draw the contours
            cv.drawContours(frame, [cnt], -1, (255, 255, 0), 2)
            ball_detected = True
            break
        else:
            continue

    cv.imshow('Frame', frame)


while True:
    ret, frame = cap.read()
    if frame is None:
        break
    process_frame(frame)
    if ball_detected or (cv.waitKey(1) & 0xFF == ord('q')):
        break

print(ball_coords)

# Release the video capture object and close any open windows
cap.release()
cv.destroyAllWindows()
