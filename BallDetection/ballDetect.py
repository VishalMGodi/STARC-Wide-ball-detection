import numpy as np
import cv2

template = cv2.resize(cv2.imread(r'Dataset\ballDataset\9Ball.png', 0), (0, 0), fx=0.8, fy=0.8)

methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
            cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

# Video Feed
cap = cv2.VideoCapture(r'Dataset\STARC - New Dataset\Dataset\New_5_MainView.mp4')
while cap.isOpened():
    ret, img = cap.read()
    img = cv2.resize(img, (0, 0), fx=0.8, fy=0.8)
    img2 = img.astype(np.uint8)  # Convert frame to 8-bit unsigned format
    h, w = template.shape

    for method in methods:
        result = cv2.matchTemplate(img2, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            location = min_loc
        else:
            location = max_loc

        bottom_right = (location[0] + w, location[1] + h)
        cv2.rectangle(img2, location, bottom_right, 255, 5)

    cv2.imshow('Ball Detection', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
