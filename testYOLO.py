from ultralytics import YOLO
import cv2 as cv

model = YOLO("yolov8n.pt")

# Read batview
video_path = '/Users/varun/Desktop/Projects/STARC-Wide-ball-detection/Dataset/New_8_BatView.mp4'

results = model.predict(source=video_path, show=True, retina_masks=True, conf=0.03, classes=[32])  # save predictions as labels
print(results)  # print img1 predictions (pixels)