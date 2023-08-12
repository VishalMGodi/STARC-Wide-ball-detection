from cvzone.PoseModule import PoseDetector
import cv2
import socket

# Params
width, height = 1280,720
video_num = 6

# Webcam
# cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(f'Dataset/New Video Dataset/Dataset/New_{video_num}_BatView.mp4')
cap = cv2.VideoCapture(f'Dataset/New Video Dataset/Dataset/New_{video_num}_MainView.mp4')
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
temp = False

while True:
    ret2, img2 = cap2.read() # Bat View
    ret, img = cap.read() # Main View

    if not ret or not ret2:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # * Resolution resized to 540x960
    img2 = cv2.resize(img2,(0,0),None,0.5,0.5)
    img = cv2.resize(img,(0,0),None,0.5,0.5)

    # Blur the image for better accuracy
    # img = cv2.GaussianBlur(img, (9,9), 0)
    img2 = cv2.GaussianBlur(img2, (11,11), 0)

    
    img2 = detector2.findPose(img2)
    img = detector.findPose(img)
    data = []

    lmList, bboxInfo = detector.findPosition(img, draw=False, bboxWithHands=False)
    lmList2, bboxInfo2 = detector2.findPosition(img2, draw=False, bboxWithHands=False)

    # print(lmList)
    # print("________________________________________________________________________________________________________________________________")
    # print(lmList2)
    # print("________________________________________________________________________________________________________________________________")
    # print(list(zip(lmList, lmList2)))

    if(lmList):
        for lm,lm2 in list(zip(lmList, lmList2)):
            data.extend([lm2[1],height - lm2[2],lm[1]])
        sock.sendto(str.encode(str(data)),serverPort)
        
    cv2.imshow("Image", img)
    cv2.imshow("MainView", img2)

    if cv2.waitKey(1) & 0xFF == ord('b'):
        temp = True

    while temp:
        if cv2.waitKey(1) & 0xFF == ord('b'):
            temp = False
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('r'):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # break
            continue

cap.release()
cv2.destroyAllWindows()