# # import socket, cv2, pickle, struct, imutils
# #
# # # Socket Create
# # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # host_name = socket.gethostname()
# # host_ip = socket.gethostbyname(host_name)
# # print('HOST IP:', host_ip)
# # port = 9999
# # socket_address = (host_ip, port)
# #
# # # Socket Bind
# # server_socket.bind(socket_address)
# #
# # # Socket Listen
# # server_socket.listen(5)
# # print("LISTENING AT:", socket_address)
# #
# # # Socket Accept
# # while True:
# #     client_socket, addr = server_socket.accept()
# #     print('GOT CONNECTION FROM:', addr)
# #     if client_socket:
# #         vid = cv2.VideoCapture(0)
# #
# #         while (vid.isOpened()):
# #             img, frame = vid.read()
# #             # frame = imutils.resize(frame, width=320)
# #             a = pickle.dumps(frame)
# #             message = struct.pack("Q", len(a)) + a
# #             client_socket.sendall(message)
# #
# #             cv2.imshow('TRANSMITTING VIDEO', frame)
# #             if cv2.waitKey(1) == '13':
# #                 client_socket.close()
#
# import cv2
# import threading
# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
#
#
# class WebcamApp:
#     def __init__(self, window, window_title):
#         self.window = window
#         self.window.title(window_title)
#
#         self.cap = cv2.VideoCapture(0)
#         self.frames = []
#
#         self.video_label = tk.Label(window)
#         self.video_label.pack()
#
#         self.record_button = tk.Button(window, text="Start Recording", command=self.toggle_record)
#         self.record_button.pack()
#
#         self.slider = ttk.Scale(window, from_=0, to=0, orient="horizontal", command=self.update_frame)
#         self.slider.pack()
#
#         self.update()
#
#     def toggle_record(self):
#         if not self.frames:
#             threading.Thread(target=self.record).start()
#
#     def record(self):
#         while True:
#             ret, frame = self.cap.read()
#             if ret:
#                 self.frames.append(frame.copy())
#                 self.slider.config(to=len(self.frames) - 1)
#                 # self.update_frame(len(self.frames) - 1)
#                 # print(len(self.frames))
#
#     def update(self):
#         if self.frames:
#             frame = self.frames[-1]
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = Image.fromarray(frame)
#             imgtk = ImageTk.PhotoImage(image=img)
#             self.video_label.imgtk = imgtk
#             self.video_label.config(image=imgtk)
#
#         self.window.after(10, self.update)
#
#     def update_frame(self, value):
#         index = int(value)
#         if 0 <= index < len(self.frames):
#             frame = self.frames[index]
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = Image.fromarray(frame)
#             imgtk = ImageTk.PhotoImage(image=img)
#             self.video_label.imgtk = imgtk
#             self.video_label.config(image=imgtk)
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = WebcamApp(root, "Webcam App")
#     root.mainloop()

# import streamlit
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
                max_frames = len(self.frames1) - 1
                self.frames1.append(frame1.copy())#adds it
                self.frames2.append(frame2.copy())#adds it

                if not self.is_recording:
                    self.slider.setMaximum(len(self.frames1) - 1)
                    self.slider.setValue(len(self.frames1) - 1)
                # else: self.slider.setValue(min(self.slider.value()+1)
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
