from cvzone.PoseModule import PoseDetector
import cv2
import socket

# Params
width, height = 1280,720 

# Webcam
cap = cv2.VideoCapture(r'Dataset\STARC - New Dataset\Dataset\New_5_MainView.mp4')
cap.set(3,width)
cap.set(4,height)

# Hand Tracking
detector = PoseDetector()

# Communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverPort = ('localhost',10000)

while True:
    success, img = cap.read()
    img = cv2.resize(img,(0,0),None,0.5,0.5)

    img = detector.findPose(img)

    if not success:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    data = []

    lmList, bboxInfo = detector.findPosition(img, draw=False, bboxWithHands=False)

    if(lmList):
        for lm in lmList:
            data.extend([lm[1],height - lm[2],lm[3]])

        sock.sendto(str.encode(str(data)),serverPort)
    
    # try:    
    #     print(f"\r{lmList[30]}",end='')
    # except Exception as e:
    #     print("\nNose Out of range...\n")

    

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()