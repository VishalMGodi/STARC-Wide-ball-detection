import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

# Params
width, height = 1280,720 

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

# Hand Tracking
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverPort = ('localhost',10000)


while True:
    # Get frame from capture
    success,img = cap.read()
    # Hands
    hands, img = detector.findHands(img)

    data = []

    # Landmark Values - (x,y,z) * 21
    if hands:
        # Get first hand detected
        hand = hands[0]
        lmlist = hand['lmList']
        # print(lmlist)
        for lm in lmlist:
            data.extend([lm[0],height - lm[1],lm[2]])
        sock.sendto(str.encode(str(data)),serverPort)

    cv2.imshow("image",img)
    cv2.waitKey(1)