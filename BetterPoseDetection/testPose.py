from vpython import *
from pynput import keyboard
from win32api import GetSystemMetrics
import mediapipe as mp
import cv2

# Get Computer Screen width and height
scene.width = GetSystemMetrics(0) - GetSystemMetrics(0)/10
scene.height = GetSystemMetrics(1) - GetSystemMetrics(1)/4

scale = 100 # 1 meter = 100 pixels
camera_speed = 20
batsmanScale = 0 # IDEALLY 140

## [IMP] in vector(x,y,z) +x #, -x #
## [IMP] in vector(x,y,z) +y moves down, -y moves up
## [IMP] in vector(x,y,z) +z #, -z #


# CAMERA CONSTANTS
CAMERA_X, CAMERA_Y, CAMERA_Z = 1317.53, 98.7792, -0.00636476
cameraCenter = vector(0,0,0)
initial_camera_pos = vector(CAMERA_X, CAMERA_Y, CAMERA_Z)


# Constants
grass_length = 23 * scale
grass_width = 5 * scale
pitch_length = 22.56 * scale
pitch_width = 3.05 * scale
popping_crease_length = 0.05 * scale
popping_crease_width = 3.05 * scale
bowling_crease_length = 0.05 * scale
bowling_crease_width = 2.64 * scale
return_crease_length = 2.44 * scale
return_crease_width = 0.05 * scale
guide_line_length = 1.22 * scale
guide_line_width = 0.05 * scale
stump_height = 0.7112 * scale
stump_radius = 0.017465 * scale
stump_spacing = 54/1000 * scale

# Create a mediapipe drawing object for drawing landmarks
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# Initialize the MediaPipe Pose model
mp_pose = mp.solutions.pose.Pose()

# Start the webcam feed
cap = cv2.VideoCapture(0)

# Define the pitch
grass = box(pos=vector(0, 0, 0), length=grass_length, height=0.1, width=grass_width, color=color.green)
pitch = box(pos=vector(0, 0.1, 0), length=pitch_length, height=0.1, width=pitch_width, color=color.yellow)

# Draw the popping creases
popping_crease1 = box(pos=vector((17.68/2) * scale, 0.2, 0), length=popping_crease_length, height=0.1, width=popping_crease_width, color=color.blue)
popping_crease2 = box(pos=vector(-(17.68/2) * scale, 0.2, 0), length=popping_crease_length, height=0.1, width=popping_crease_width, color=color.blue)

# Draw the bowling creases
bowling_crease1 = box(pos=vector((17.68/2 + 1.22) * scale, 0.2, 0), length=bowling_crease_length, height=0.1, width=bowling_crease_width, color=color.blue)
bowling_crease2 = box(pos=vector(-(17.68/2 + 1.22) * scale, 0.2, 0), length=bowling_crease_length, height=0.1, width=bowling_crease_width, color=color.blue)

# Draw the return creases
return_crease1 = box(pos=vector((17.68/2 + 1.22) * scale, 0.2, 1.32 * scale), length=return_crease_length, height=0.1, width=return_crease_width, color=color.blue)
return_crease2 = box(pos=vector((17.68/2 + 1.22) * scale, 0.2, -1.32 * scale), length=return_crease_length, height=0.1, width=return_crease_width, color=color.blue)
return_crease3 = box(pos=vector(-(17.68/2 + 1.22) * scale, 0.2, 1.32 * scale), length=return_crease_length, height=0.1, width=return_crease_width, color=color.blue)
return_crease4 = box(pos=vector(-(17.68/2 + 1.22) * scale, 0.2, -1.32 * scale), length=return_crease_length, height=0.1, width=return_crease_width, color=color.blue)

# Draw the guide lines
guide_line1 = box(pos=vector((17.68/2 + 1.22/2) * scale, 0.2, 0.89 * scale), length=guide_line_length, height=0.1, width=guide_line_width, color=color.blue)
guide_line2 = box(pos=vector((17.68/2 + 1.22/2) * scale, 0.2, -0.89 * scale), length=guide_line_length, height=0.1, width=guide_line_width, color=color.blue)
guide_line3 = box(pos=vector(-(17.68/2 + 1.22/2) * scale, 0.2, 0.89 * scale), length=guide_line_length, height=0.1, width=guide_line_width, color=color.blue)
guide_line4 = box(pos=vector(-(17.68/2 + 1.22/2) * scale, 0.2, -0.89 * scale), length=guide_line_length, height=0.1, width=guide_line_width, color=color.blue)

# Draw the stumps
stump11 = cylinder(pos=vector((17.68/2 + 1.22) * scale, 0.3, 0), axis=vector(0, 1, 0), radius=stump_radius, length=stump_height, color=color.white)
stump12 = cylinder(pos=vector((17.68/2 + 1.22) * scale, 0.3, stump_spacing+2*stump_radius), axis=vector(0, 1, 0), radius=stump_radius, length=stump_height, color=color.white)
stump13 = cylinder(pos=vector((17.68/2 + 1.22) * scale, 0.3, -(stump_spacing+2*stump_radius)), axis=vector(0, 1, 0), radius=stump_radius, length=stump_height, color=color.white)

stump21 = cylinder(pos=vector(-(17.68/2 + 1.22) * scale, 0.3, 0), axis=vector(0, 1, 0), radius=stump_radius, length=stump_height, color=color.white)
stump22 = cylinder(pos=vector(-(17.68/2 + 1.22) * scale, 0.3, stump_spacing+2*stump_radius), axis=vector(0, 1, 0), radius=stump_radius, length=stump_height, color=color.white)
stump23 = cylinder(pos=vector(-(17.68/2 + 1.22) * scale, 0.3, -(stump_spacing+2*stump_radius)), axis=vector(0, 1, 0), radius=stump_radius, length=stump_height, color=color.white)

# Draw the Batsman (Using Nose for development, change NOSE to RIGHT_HEEL)
ballSize = 0.1
batsmanNose = sphere(pos = cameraCenter, radius=0.1 * scale, color=color.red)

# Initialize the camera
scene.camera.pos = initial_camera_pos
scene.camera.rotate(1.5708 , vector(0, 1, 0))
centerBall = sphere(pos = cameraCenter,radius = 0.1*scale, color = color.white)
scene.center = centerBall.pos

# scene.autoscale = False
# scene.center = initial_camera_pos

# Test Buttons
def addBatsmanScale():
    global batsmanScale
    batsmanScale += 10
    print(f"batsmanScale: {batsmanScale}")
button( bind = addBatsmanScale, text='+10 batsmanScale' )

def subBatsmanScale():
    global batsmanScale
    batsmanScale -= 10
    print(f"batsmanScale: {batsmanScale}")
button( bind = subBatsmanScale, text='-10 batsmanScale' )

def changeBallSize():
    global ballSize
    batsmanNose.radius -= 0.01*scale
    print(f"batsmanNoseRadius: {batsmanNose}")
button( bind = changeBallSize, text='-0.01 ballSize' )

# Move the camera on WASD keys
def keyInput(key):
    global camera_speed
    camera_pos_rel = scene.camera.pos
    camera_axis = scene.camera.axis.norm()

    try:
        if key.char == "w":
            camera_pos_rel += camera_axis * camera_speed
        elif key.char == 's':
            camera_pos_rel -= camera_axis * camera_speed
        elif key.char == 'a':
            camera_pos_rel -= cross(camera_axis, vector(0, 1, 0)).norm() * camera_speed
        elif key.char == 'd':
            camera_pos_rel += cross(camera_axis, vector(0, 1, 0)).norm() * camera_speed
        elif key.char == 'r':
            scene.center = centerBall.pos
            return
    except AttributeError:
        if key == keyboard.Key.space:
            camera_pos_rel += vector(0, 1, 0) * camera_speed
        elif key == keyboard.Key.shift:
            camera_pos_rel -= vector(0, 1, 0) * camera_speed
    # print(f"{camera_pos_rel}")
    scene.camera.pos = camera_pos_rel


listener = keyboard.Listener(on_press=keyInput)
listener.start()
initialFrameFlag = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_pose.process(frame_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        if not initialFrameFlag:
            initX = landmarks[mp.solutions.pose.PoseLandmark.NOSE].x
            initY = landmarks[mp.solutions.pose.PoseLandmark.NOSE].y
            initialFrameFlag = 1
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        print(f"\rNOSE COORDS {mp.solutions.pose.PoseLandmark.NOSE}: {round(landmarks[mp.solutions.pose.PoseLandmark.NOSE].x,2)},{round(landmarks[mp.solutions.pose.PoseLandmark.NOSE].y,2)},{round(landmarks[mp.solutions.pose.PoseLandmark.NOSE].z,2)}", end='', flush=True)
        # Get the position of a specific landmark (e.g., nose) & update the pose object's position in VPython
        batsmanNose.pos = vector(0,
                                 0,
                                 (initX - landmarks[mp.solutions.pose.PoseLandmark.NOSE].x) * batsmanScale)
    cv2.namedWindow("MediaPipe Pose", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("MediaPipe Pose", 800,600)
    cv2.imshow('MediaPipe Pose', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        batsmanNose.pos = vector(0,0,0)
        break
    rate(45)

mp_pose.close()
cap.release()
cv2.destroyAllWindows()

