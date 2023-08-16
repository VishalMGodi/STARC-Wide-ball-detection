from cvzone.PoseModule import PoseDetector
import cv2
import socket

def runPose(video_path_bat, video_path_main, stop_frame_number):
    
    # Params
    width, height = 1280,720

    # Read video
    # cap = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(video_path_bat) # f'Dataset/New Video Dataset/Dataset/New_{video_num}_BatView.mp4')
    cap = cv2.VideoCapture(video_path_main) # f'Dataset/New Video Dataset/Dataset/New_{video_num}_MainView.mp4')
    cap.set(3,width)
    cap.set(4,height)
    cap2.set(3,width)
    cap2.set(4,height)

    # Pose Tracking
    detector = PoseDetector(detectionCon = 0.8, trackCon = 0.8, smooth = False)
    detector2 = PoseDetector()

    # Communication
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverPort = ('localhost',10000)

    # While current frame number is less that stop frame number
    while cap.get(cv2.CAP_PROP_POS_FRAMES) <= stop_frame_number:
        ret2, img2 = cap2.read() # Bat View
        ret, img = cap.read() # Main View

        # Reset frames after completion
        if not ret or not ret2:
            break

        # * Resolution resized to 540x960
        img2 = cv2.resize(img2,(0,0),None,0.5,0.5)
        img = cv2.resize(img,(0,0),None,0.5,0.5)

        # Blur the image for better accuracy
        img = cv2.GaussianBlur(img, (9,9), 0)
        img2 = cv2.GaussianBlur(img2, (11,11), 0)

        
        img2 = detector2.findPose(img2)
        img = detector.findPose(img)
        data = []

        lmList, bboxInfo = detector.findPosition(img, draw=False, bboxWithHands=False)
        lmList2, bboxInfo2 = detector2.findPosition(img2, draw=False, bboxWithHands=False)

        if __name__ == '__main__':
            cv2.imshow('MainView',img)
            cv2.imshow('BatView',img2)
            cv2.waitKey(0)


        if(lmList):
            for lm,lm2 in list(zip(lmList, lmList2)):
                data.extend([lm2[1],height - lm2[2],lm[1]])
            sock.sendto(str.encode(str(data)),serverPort)


if __name__ == '__main__':
    mainPath = "/Users/varun/Desktop/Projects/STARC-Wide-ball-detection/Dataset/New_5_MainView.mp4"
    batPath = "/Users/varun/Desktop/Projects/STARC-Wide-ball-detection/Dataset/New_5_BatView.mp4"

    runPose(mainPath, batPath, 328)