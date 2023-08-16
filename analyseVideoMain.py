import cv2 as cv
import numpy as np

def runMain(last_detection_frame, buffer, video_path):

    # Video file path
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

        print(f"Current frame: {current_frame_number}", end="\r")

        if abs(current_frame_number - last_detection_frame) <= buffer:  # You can adjust the threshold as needed
        # if True:
            # Resize the frame
            frame = cv.resize(frame, (1920, 1080), fx=0, fy=0, interpolation=cv.INTER_CUBIC) 
            process_frame(frame)


    # Release the video capture object and close any open windows
    cap.release()
    cv.destroyAllWindows()

    return ball_coords

if __name__ == "__main__":
    print(runMain(0, 40, f"/Users/varun/Desktop/Projects/STARC-Wide-ball-detection/Dataset/New_{(input('Enter Video number: '))}_MainView.mp4"))