import cv2
import threading
import sys, time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer
from PIL import Image
import numpy as np

from analyseVideo import BatMan

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Video codec
output_filename1 = "VIEW1.mp4"
output_filename2 = "VIEW2.mp4"
datasetpath = "/Users/varun/Desktop/Projects/STARC-Wide-ball-detection/Dataset/"

margin = 10
vid_w = 640 #1920#640
vid_h = 360 #1080#480
btn_w = 120
btn_h = 30
slider_width = vid_w+margin+vid_w
clr_red = QtGui.QColor("red")
clr_green = QtGui.QColor("green")


class WebcamApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # self.cap = cv2.VideoCapture(0)
        self.cap_main = cv2.VideoCapture(datasetpath+"New_5_MainView.mp4")
        self.cap_bat = cv2.VideoCapture(datasetpath+"New_5_BatView.mp4")

        # cv2.imshow("Main", self.cap_main.read()[1])
        # cv2.imshow("Bat", self.cap_bat.read()[1])
        # cv2.waitKey(0)

        # self.cap_bat = self.cap_main = cv2.VideoCapture(0)
        self.frames1 = []#(1080, 1920, 3) (1080, 1920, 3)
        self.frames2 = []
        self.clip = [-1,-1]
        self.is_recording = False

        self.video_label1 = QtWidgets.QLabel(self)
        self.video_label1.setGeometry(margin, margin, vid_w, vid_h) # x, y, w, h

        self.video_label2 = QtWidgets.QLabel(self)
        self.video_label2.setGeometry(margin+vid_w+margin, margin, vid_w, vid_h)

        self.record_button = QtWidgets.QPushButton("Clip", self)
        self.record_button.setGeometry(margin, margin+vid_h+margin, btn_w, btn_h)
        self.record_button.clicked.connect(self.toggle_record)

        self.save_button = QtWidgets.QPushButton("Predict (Save)", self)
        self.save_button.setGeometry(500, margin+vid_h+margin, btn_w, btn_h)
        self.save_button.clicked.connect(self.video)
        self.save_button.hide()

        self.mrk_strt_pt_button = QtWidgets.QPushButton("Mark as Start", self)
        self.mrk_strt_pt_button.setGeometry(200, margin+vid_h+margin, btn_w, btn_h)
        self.mrk_strt_pt_button.clicked.connect(self.mark_point_start)
        self.mrk_strt_pt_button.hide()

        self.mrk_end_pt_button = QtWidgets.QPushButton("Mark as End", self)
        self.mrk_end_pt_button.setGeometry(350, margin+vid_h+margin, btn_w, btn_h)
        self.mrk_end_pt_button.clicked.connect(self.mark_point_end)
        self.mrk_end_pt_button.hide()

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)  # Use QtCore.Qt.Horizontal
        self.slider.setGeometry(margin, margin+vid_h+margin+margin+btn_h+margin, slider_width, btn_h)
        self.slider.valueChanged.connect(self.update_frame)

        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setGeometry(margin +btn_w +margin, margin+vid_h+margin, slider_width - margin-margin-btn_w, btn_h)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

        self.label = QtWidgets.QLabel("Predicted", self)  # wide? or not?
        self.label.setGeometry(margin +btn_w +margin, margin+vid_h+margin, 380, btn_h)
        self.label.hide()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        threading.Thread(target=self.record, daemon=True).start()

    def toggle_record(self):
        if not self.is_recording:
            self.is_recording = True
            self.record_button.setText("Follow Live")
            self.mrk_strt_pt_button.show()
            self.mrk_end_pt_button.show()
            # self.save_button.show()
            # self.frames = []
        else:
            self.is_recording = False
            self.record_button.setText("Clip")
            self.mrk_strt_pt_button.hide()
            self.mrk_end_pt_button.hide()
            self.save_button.hide()
            self.clip = [-1, -1]

    def record(self):
        # while self.is_recording:
        while True:
            ret1, frame1 = self.cap_main.read() # gets new frame
            ret2, frame2 = self.cap_bat.read() # gets new frame
            if ret1 and ret2:
                # print(frame1.shape, frame2.shape)
                max_frames = len(self.frames1) - 1
                self.frames1.append(frame1.copy())#adds it
                self.frames2.append(frame2.copy())#adds it

                if not self.is_recording:
                    self.slider.setMaximum(max_frames)
                    self.slider.setValue(max_frames)
                    self.update_frame(max_frames)
                # else: self.slider.setValue(min(self.slider.value()+1)

    def update(self):
        if self.frames1 and self.frames2:
            # print(self.slider.value())
            ndx = self.slider.value()
            cv2.resize(self.frames1[ndx], (640, 360))
            image1 = Image.fromarray(
                cv2.cvtColor(cv2.resize(self.frames1[ndx], (640, 360)), cv2.COLOR_BGR2RGB)
            )
            image2 = Image.fromarray(
                cv2.cvtColor(cv2.resize(self.frames2[ndx], (640, 360)), cv2.COLOR_BGR2RGB)
            )
            self.video_label1.setPixmap(
                QtGui.QPixmap.fromImage(
                    QtGui.QImage(image1.tobytes(), image1.width, image1.height, QtGui.QImage.Format_RGB888)
                )
            )
            self.video_label2.setPixmap(
                QtGui.QPixmap.fromImage(
                    QtGui.QImage(image2.tobytes(), image2.width, image2.height, QtGui.QImage.Format_RGB888)
                )
            )

    def paintEvent(self, event):
        # print("called")
        max_val = self.slider.maximum()
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(clr_green, 5, QtCore.Qt.SolidLine))
        if self.clip[0] != -1:
            s_val = int((self.clip[0] / max_val) * slider_width) + margin
            painter.drawLine(
                QtCore.QPoint(s_val, margin + vid_h + margin + margin + btn_h + margin),
                QtCore.QPoint(s_val, margin + vid_h + margin + margin + btn_h + margin + 50)
            )
        painter.setPen(QtGui.QPen(clr_red, 5, QtCore.Qt.SolidLine))
        if self.clip[1] != -1:
            e_val = int((self.clip[1] / max_val) * slider_width) + margin
            painter.drawLine(
                QtCore.QPoint(e_val, margin + vid_h + margin + margin + btn_h + margin),
                QtCore.QPoint(e_val, margin + vid_h + margin + margin + btn_h + margin + 50)
            )

    def update_frame(self, value):
        index = int(value)
        if 0 <= index < len(self.frames1) <= len(self.frames2):
            image1 = Image.fromarray(
                cv2.cvtColor(cv2.resize(self.frames1[index], (640, 360)), cv2.COLOR_BGR2RGB)
            )
            image2 = Image.fromarray(
                cv2.cvtColor(cv2.resize(self.frames2[index], (640, 360)), cv2.COLOR_BGR2RGB)
            )
            self.video_label1.setPixmap(
                QtGui.QPixmap.fromImage(
                    QtGui.QImage(image1.tobytes(), image1.width, image1.height, QtGui.QImage.Format_RGB888)
                )
            )
            self.video_label2.setPixmap(
                QtGui.QPixmap.fromImage(
                    QtGui.QImage(image2.tobytes(), image2.width, image2.height, QtGui.QImage.Format_RGB888)
                )
            )

    def mark_point_start(self):
        self.clip[0] = self.slider.value()
        if self.clip[1] != -1 and self.clip[0] < self.clip[1]:
            self.save_button.show()

    def mark_point_end(self):
        self.clip[1] = self.slider.value()
        if self.clip[0] != -1 and self.clip[0] < self.clip[1]:
            self.save_button.show()

    def callRunBat(self, obj:BatMan, output_file):
        # for i in range(100):
        #     obj.shared_variable = i
        #     time.sleep(0.1)
        ball_detected = obj.runBat(output_file)

    def video(self):
        frm, to = self.clip
        self.save_button.hide()
        self.mrk_end_pt_button.hide()
        self.mrk_strt_pt_button.hide()

        ht1, wdth1, layers1 = self.frames1[0].shape
        ht2, wdth2, layers2 = self.frames2[0].shape
        out1 = cv2.VideoWriter(output_filename1, fourcc, 30, (wdth1, ht1))
        out2 = cv2.VideoWriter(output_filename2, fourcc, 30, (wdth2, ht2))

        for frame in self.frames1[frm:to+1]: # Write each frame to the video file
            out1.write(frame)
        out1.release() # Release the VideoWriter object and close the video file

        for frame in self.frames2[frm:to+1]: # Write each frame to the video file
            out2.write(frame)
        out2.release() # Release the VideoWriter object and close the video file

        print("Videos saved as", output_filename1,"and", output_filename2)
        self.progress_bar.show()

        bat_obj = BatMan()
        bat_view_thread = threading.Thread(target=self.callRunBat, args=(bat_obj, output_filename2,), daemon=True)
        bat_view_thread.start()

        progress_value = int(bat_obj.shared_variable*100)

        while progress_value<100:
            print("Progress value:", progress_value)
            self.progress_bar.setValue(progress_value)
            # time.sleep(0.1)
            # progress_value+=1
            progress_value = int(bat_obj.shared_variable*100)
        self.progress_bar.setValue(100)
        # self.progress_bar.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    print("Starting app")
    window = WebcamApp()
    print("Starting webcam")
    window.show()
    print("Starting window.show")
    sys.exit(app.exec_())
