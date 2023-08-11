import cv2 as cv
import numpy as np

def runBat():
    # Video file path
    video_path = '/Users/varun/Desktop/Projects/STARC-Wide-ball-detection/Dataset/New_5_BatView.mp4'
    cap = cv.VideoCapture(video_path)

    # Create the background subtractor object
    object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    #Make a set of coordinates
    ball_coords = []
    final_pos = None

    # Flag to check if ball is detected
    ball_detected = False

    def process_frame(frame):

        global ball_detected    

        # Create the mask
        mask = object_detector.apply(frame)

        # Find the contours
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:

            # Calculate the area and eliminate small contours
            area = cv.contourArea(cnt)

            # Make the main rectangle within which the objects need to be detected
            xM = int(frame.shape[1]/2.25)
            yM = int(frame.shape[0]/2)
            x2M = int(frame.shape[1]/3.0)
            y2M = int(frame.shape[0]/1.2)

            # Make a buffer rectangle within which the objects need to be detected if its not detected withing the main rectangle
            xB = 0 #int(frame.shape[1]/3.75)
            yB = int(frame.shape[0]/2)
            x2B = int(frame.shape[1])
            y2B = int(frame.shape[0]/1.2)

            # cv.rectangle(frame, (xM, yM), (x2M, y2M), (0, 255, 0), 2)
            # cv.rectangle(frame, (xB, yB), (x2B, y2B), (0, 0, 255), 4)

            if area < 100:
                continue

            # Draw the rectangles

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
            if (frame[cnt[0][0][1]][cnt[0][0][0]][2] < 95) or (frame[cnt[0][0][1]][cnt[0][0][0]][2] > 106):
                continue

            if (frame[cnt[0][0][1]][cnt[0][0][0]][1] < 75) or (frame[cnt[0][0][1]][cnt[0][0][0]][1] > 90):
                continue

            if (frame[cnt[0][0][1]][cnt[0][0][0]][0] < 53) or (frame[cnt[0][0][1]][cnt[0][0][0]][0] > 75):
                continue

            # check if the contour is within the main rectangle
            if (cnt[0][0][0] > xM) and (cnt[0][0][0] < x2M) and (cnt[0][0][1] > yM) and (cnt[0][0][1] < y2M):
                ball_coords.append((cv.boundingRect(cnt), "Main", int(cap.get(cv.CAP_PROP_POS_FRAMES))))
                ball_detected = True
                break

            # Check if its within the buffer rectangle
            elif (cnt[0][0][0] > xB) and (cnt[0][0][0] < x2B) and (cnt[0][0][1] > yB) and (cnt[0][0][1] < y2B):
                ball_coords.append((cv.boundingRect(cnt), "Buffer", int(cap.get(cv.CAP_PROP_POS_FRAMES))))

                if(cnt[0][0][0] < x2M):
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
        if ball_detected:

            # Draw boxes for all the coordinates      
            for i, coord in enumerate(ball_coords):
                if(coord[1] == "Main"):
                    cv.rectangle(frame, (coord[0][0], coord[0][1]), (coord[0][0]+coord[0][2], coord[0][1]+coord[0][3]), (0, 0, 255))
                elif(coord[1] == "Buffer"):
                    cv.rectangle(frame, (coord[0][0], coord[0][1]), (coord[0][0]+coord[0][2], coord[0][1]+coord[0][3]), (255, 255, 0))
            cv.imshow('Frame', frame)
            # if (cv.waitKey(0) & 0xFF == ord('q')):
            #     break
            # break
        if (cv.waitKey(1) & 0xFF == ord('q')):
            break

    final_pos = ball_coords[-1]

    # Release the video capture object and close any open windows
    cap.release()
    cv.destroyAllWindows()

    return final_pos
