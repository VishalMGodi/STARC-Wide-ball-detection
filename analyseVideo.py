import cv2 as cv
import numpy as np

class BatMan:
    def __init__(self) -> None:
        self.shared_variable = 0

    def runBat(self, video_path):
        # Video file path
        cap = cv.VideoCapture(video_path)
        cap.set(3, 1920)
        cap.set(4, 1080)

        # Create the background subtractor object
        object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

        #Make a set of coordinates
        ball_detected = None

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
                xB = int(frame.shape[1]/3.75)
                yB = int(frame.shape[0]/2)
                x2B = int(frame.shape[1])
                y2B = int(frame.shape[0]/1.2)

                if area < 100:
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
                if (frame[cnt[0][0][1]][cnt[0][0][0]][2] < 95) or (frame[cnt[0][0][1]][cnt[0][0][0]][2] > 106):
                    continue

                if (frame[cnt[0][0][1]][cnt[0][0][0]][1] < 75) or (frame[cnt[0][0][1]][cnt[0][0][0]][1] > 90):
                    continue

                if (frame[cnt[0][0][1]][cnt[0][0][0]][0] < 53) or (frame[cnt[0][0][1]][cnt[0][0][0]][0] > 75):
                    continue

                # check if the contour is within the main rectangle
                if (cnt[0][0][0] > xM) and (cnt[0][0][0] < x2M) and (cnt[0][0][1] > yM) and (cnt[0][0][1] < y2M):
                    print(f"Ball detected in frame {int(cap.get(cv.CAP_PROP_POS_FRAMES))} in Main Rectangle")
                    return (cv.boundingRect(cnt), "Main", int(cap.get(cv.CAP_PROP_POS_FRAMES)))

                # Check if its within the buffer rectangle
                elif (cnt[0][0][0] > xB) and (cnt[0][0][0] < x2B) and (cnt[0][0][1] > yB) and (cnt[0][0][1] < y2B):
                    if(cnt[0][0][0] < x2M):
                        print(f"Ball detected in frame {int(cap.get(cv.CAP_PROP_POS_FRAMES))} in Main Rectangle")
                        return (cv.boundingRect(cnt), "Buffer", int(cap.get(cv.CAP_PROP_POS_FRAMES)))
            return None

        while True:
            ret, frame = cap.read()
            if frame is None:
                self.shared_variable = 1
                break

            ball_detected = process_frame(frame)
            self.shared_variable = int(cap.get(cv.CAP_PROP_POS_FRAMES))/int(cap.get(cv.CAP_PROP_FRAME_COUNT))

            print(f"Current frame: {int(cap.get(cv.CAP_PROP_POS_FRAMES))} / {int(cap.get(cv.CAP_PROP_FRAME_COUNT))}\t\tBall detected: {not not ball_detected}", end="\r")

            if ball_detected:
                self.shared_variable = 1
                break

        # Release the video capture object and close any open windows
        cap.release()
        cv.destroyAllWindows()

        return ball_detected
    
if __name__ == "__main__":
    batman = BatMan()
    batman.runBat("/Users/varun/Desktop/Projects/STARC-Wide-ball-detection/Dataset/New_5_BatView.mp4")
