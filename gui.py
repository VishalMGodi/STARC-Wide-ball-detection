import cv2
import threading
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer
from PIL import Image
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Video codec
output_filename1 = "VIEW1.mp4"
output_filename2 = "VIEW2.mp4"


class WebcamApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.cap = cv2.VideoCapture(0)
        self.frames1 = []
        self.frames2 = []
        self.clip = [0,0]
        self.is_recording = False

        self.video_label1 = QtWidgets.QLabel(self)
        self.video_label1.setGeometry(10, 10, 640, 480)

        self.video_label2 = QtWidgets.QLabel(self)
        self.video_label2.setGeometry(660, 10, 640, 480)

        self.record_button = QtWidgets.QPushButton("Start Recording", self)
        self.record_button.setGeometry(10, 500, 120, 30)
        self.record_button.clicked.connect(self.toggle_record)

        self.save_button = QtWidgets.QPushButton("Predict (Save)", self)
        self.save_button.setGeometry(500, 500, 120, 30)
        self.save_button.clicked.connect(self.video)
        self.save_button.hide()

        self.mrk_strt_pt_button = QtWidgets.QPushButton("Mark as Start", self)
        self.mrk_strt_pt_button.setGeometry(200, 500, 120, 30)
        self.mrk_strt_pt_button.clicked.connect(self.mark_point_start)
        self.mrk_strt_pt_button.hide()

        self.mrk_end_pt_button = QtWidgets.QPushButton("Mark as End", self)
        self.mrk_end_pt_button.setGeometry(350, 500, 120, 30)
        self.mrk_end_pt_button.clicked.connect(self.mark_point_end)
        self.mrk_end_pt_button.hide()

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)  # Use QtCore.Qt.Horizontal
        self.slider.setGeometry(10, 550, 1280, 30)
        self.slider.valueChanged.connect(self.update_frame)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        threading.Thread(target=self.record, daemon=True).start()

    def toggle_record(self):
        if not self.is_recording:
            self.is_recording = True
            self.record_button.setText("Stop Recording")
            self.mrk_strt_pt_button.show()
            self.mrk_end_pt_button.show()
            # self.save_button.show()
            # self.frames = []
        else:
            self.is_recording = False
            self.record_button.setText("Start Recording")
            self.mrk_strt_pt_button.hide()
            self.mrk_end_pt_button.hide()
            self.save_button.hide()
            self.clip = [0, 0]

    def record(self):
        # while self.is_recording:
        while True:
            ret1, frame1 = self.cap.read()#gets new frame
            ret2, frame2 = self.cap.read()  # gets new frame
            if ret1 and ret2:
                self.frames1.append(frame1.copy())#adds it
                self.frames2.append(frame2.copy())#adds it
                self.slider.setMaximum(len(self.frames1) - 1)
                if not self.is_recording:
                    self.slider.setValue(len(self.frames1) - 1)
                self.update_frame(len(self.frames1) - 1)

    def update(self):
        if self.frames1 and self.frames2:
            # frame = cv2.cvtColor(self.frames[-1], cv2.COLOR_BGR2RGB)
            # print(self.slider.value())
            image1 = Image.fromarray(
                cv2.cvtColor(self.frames1[self.slider.value()], cv2.COLOR_BGR2RGB)
            )
            image2 = Image.fromarray(
                cv2.cvtColor(self.frames2[self.slider.value()], cv2.COLOR_BGR2RGB)
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

    def update_frame(self, value):
        index = int(value)
        if 0 <= index < len(self.frames1) <= len(self.frames2):
            image1 = Image.fromarray(
                cv2.cvtColor(self.frames1[index], cv2.COLOR_BGR2RGB)
            )
            image2 = Image.fromarray(
                cv2.cvtColor(self.frames2[index], cv2.COLOR_BGR2RGB)
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = WebcamApp()
    window.show()
    sys.exit(app.exec_())
