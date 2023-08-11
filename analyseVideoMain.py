import cv2 as cv
import numpy as np

from analyseVideo import runBat

import socket

def runMain(last_detection_frame, buffer):

    # Video file path
    video_path = '/Users/varun/Desktop/Projects/STARC-Wide-ball-detection/Dataset/New_5_MainView.mp4'
    cap = cv.VideoCapture(video_path)
    cap.set(3, 1920)
    cap.set(4, 1080)

    # Move to the last detection frame
    cap.set(cv.CAP_PROP_POS_FRAMES, last_detection_frame-buffer//2)

    print(f"Current frame number: {int(cap.get(cv.CAP_PROP_POS_FRAMES))}")

    # Create the background subtractor object
    object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    #Make a set of coordinates
    ball_coords = []

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
            ball_coords.append((cv.boundingRect(cnt), "Main", int(cap.get(cv.CAP_PROP_POS_FRAMES))))

    while True:
        ret, frame = cap.read()
        if frame is None:
            break

        current_frame_number = int(cap.get(cv.CAP_PROP_POS_FRAMES))

        if abs(current_frame_number - last_detection_frame) <= buffer:  # You can adjust the threshold as needed

            # Resize the frame
            frame = cv.resize(frame, (1920, 1080), fx=0, fy=0, interpolation=cv.INTER_CUBIC) 

            process_frame(frame)

            # # Draw boxes for all the coordinates      
            # for i, coord in enumerate(ball_coords):
            #     if(coord[1] == "Main"):
            #         cv.rectangle(frame, (coord[0][0], coord[0][1]), (coord[0][0]+coord[0][2], coord[0][1]+coord[0][3]), (0, 0, 255))
            #     elif(coord[1] == "Buffer"):
            #         cv.rectangle(frame, (coord[0][0], coord[0][1]), (coord[0][0]+coord[0][2], coord[0][1]+coord[0][3]), (255, 255, 0))

            cv.imshow('Frame', frame)

            if (cv.waitKey(1) & 0xFF == ord('q')):
                break

    # Release the video capture object and close any open windows
    cap.release()
    cv.destroyAllWindows()

    return ball_coords

if __name__ == '__main__':
    coordsBat = runBat()
    coordsMain = runMain(coordsBat[-1], 40)

    print(f"Bat View Detections: {coordsBat}\nMain View Detections: {coordsMain}")

    closest_main_view_detection = min(coordsMain, key=lambda x: abs(x[2] - coordsBat[-1]))

    print(f"Bat View Detection: {coordsBat}\nMain View Detection: {closest_main_view_detection}")

    final_ball_position = (coordsBat[0][0]+coordsBat[0][2]/2, coordsBat[0][1]+coordsBat[0][3]/2, closest_main_view_detection[0][0]+closest_main_view_detection[0][2]/2)

    print(f"Final Ball Position: {final_ball_position}")

    # Send the final ball position to the UDP server over port 11001
    UDP_IP = "localhost"
    UDP_PORT = 11001

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(str(final_ball_position).encode(), (UDP_IP, UDP_PORT))

    # Show the positions in the videos
    video_path = '/Users/varun/Desktop/Projects/STARC-Wide-ball-detection/Dataset/New_5_BatView.mp4'
    cap = cv.VideoCapture(video_path)
    cap.set(3, 1920)
    cap.set(4, 1080)

    frame_number_bat = coordsBat[2]
    cap.set(cv.CAP_PROP_POS_FRAMES, frame_number_bat)
    ret, frame = cap.read()

    xb, yb, wb, hb = coordsBat[0]
    cv.rectangle(frame, (xb, yb), (xb+wb, yb+hb), (0, 0, 255))

    cv.imshow('bat', frame)

    # Show the positions in the videos

    video_path = '/Users/varun/Desktop/Projects/STARC-Wide-ball-detection/Dataset/New_5_MainView.mp4'
    cap = cv.VideoCapture(video_path)

    frame_number_main = closest_main_view_detection[2]
    cap.set(cv.CAP_PROP_POS_FRAMES, frame_number_main)

    ret, frame = cap.read()

    xm, ym, wm, hm = closest_main_view_detection[0]
    cv.rectangle(frame, (xm, ym), (xm+wm, ym+hm), (0, 0, 255))

    cv.imshow('main', frame)

    cv.waitKey(0)


    # print(coordsMain, frame_number_main)

    # final_ball_pos = (xb+wb/2, yb+hb/2, xm+wm/2)
    # print(final_ball_pos)