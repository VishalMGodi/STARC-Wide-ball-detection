from cvzone.PoseModule import PoseDetector
import cv2
import socket

# Params
width, height = 1280,720

# Webcam
# cap = cv2.VideoCapture(r'Dataset/STARC - New Dataset/Camera Data/Calibration/MiddleWicketToWideLine.MOV')
# cap = cv2.VideoCapture(r'Dataset\STARC - New Dataset\Camera Data\Calibration\MiddleWicketToFull.MOV')
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(r'Dataset\STARC - New Dataset\Dataset\New_2_MainView.mp4')
cap.set(3,width)
cap.set(4,height)

# Hand Tracking
detector = PoseDetector()

# Communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverPort = ('localhost',10000)

while True:
    temp = True
    ret, img = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # * Resolution resized to 540x960
    img = cv2.resize(img,(0,0),None,0.5,0.5)
    img = cv2.GaussianBlur(img, (11,11), 0)

    
    img = detector.findPose(img)
    data = []

    lmList, bboxInfo = detector.findPosition(img, draw=False, bboxWithHands=False)

    if(lmList):
        for lm in lmList:
            data.extend([lm[1],height - lm[2],lm[3]])

        sock.sendto(str.encode(str(data)),serverPort)
        
    cv2.imshow("Image", img)

    # while temp:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('r'):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # break
        continue

cap.release()
cv2.destroyAllWindows()