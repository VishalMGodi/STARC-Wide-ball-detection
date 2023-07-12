from vpython import *
from pynput import keyboard
from win32api import GetSystemMetrics
import mediapipe as mp
import cv2
import math
import numpy as np
# Get Computer Screen width and height
scene.width = GetSystemMetrics(0) - GetSystemMetrics(0)/10
scene.height = GetSystemMetrics(1) - GetSystemMetrics(1)/4

scale = 100 # 1 meter = 100 pixels
camera_speed = 20
batsmanScale = 300 # IDEALLY 450, 300 for newDataset

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

# Initialize the MainWindow model
mp_pose = mp.solutions.pose.Pose()

# Start the webcam feed

cap = cv2.VideoCapture(r'Dataset\New_5_MainView.mp4')


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

# Middlestump (Bat side)
stump21 = cylinder(pos=vector(-(17.68/2 + 1.22) * scale, 0.3, 0), axis=vector(0, 1, 0), radius=stump_radius, length=stump_height, color=color.white)
# Offstump (Bat side)
stump22 = cylinder(pos=vector(-(17.68/2 + 1.22) * scale, 0.3, stump_spacing+2*stump_radius), axis=vector(0, 1, 0), radius=stump_radius, length=stump_height, color=color.white)
# Legstump (Bat Side)
stump23 = cylinder(pos=vector(-(17.68/2 + 1.22) * scale, 0.3, -(stump_spacing+2*stump_radius)), axis=vector(0, 1, 0), radius=stump_radius, length=stump_height, color=color.white)

# Draw the Batsman (Using RIGHT_FOOT_INDEX for development, change RIGHT_FOOT_INDEX to RIGHT_HEEL)
ballSize = 0.1
batsmanFoot = sphere(pos = cameraCenter+vector(-(17.68/2) * scale,0.4,0), radius=0.04 * scale, color=color.red)

# Draw the virutal wide line, which moves parallel to the batsman's foot
virtual_guide_line = box(pos=vector(-(17.68/2 + 1.22/2) * scale, 0.3, 0.89 * scale), length=guide_line_length, height=0.1, width=guide_line_width, color=color.magenta)

# Testing
# testball = sphere(pos = vector(-(17.68/2 + 1.22) * scale, 0.3, 1.32*100), radius=0.1 * scale, color=color.red)
# Initialize the camera
scene.fov = 0.8098
scene.range = 300
scene.camera.pos = initial_camera_pos
scene.camera.rotate(1.5708 , vector(0, 1, 0))
centerBall = sphere(pos = cameraCenter,radius = 0.1*scale, color = color.white)
scene.center = centerBall.pos

# scene.autoscale = False
# scene.center = initial_camera_pos

# Test Buttons
def printCameraStats():
    print("\n---------\n")
    print(f"scene.camera.pos: {scene.camera.pos}")
    print(f"scene.camera.axis: {scene.camera.axis}")
    print(f"scene.camera.up: {scene.camera.up}")
    print(f"scene.forward: {scene.forward}")
    print(f"scene.camera.center: {scene.center}")
button( bind = printCameraStats, text='Print Camera Stats' )

def startMoving():
    global temp
    temp = 0
button( bind = startMoving, text='Start' )
def stopMoving():
    global temp
    temp = 1
button( bind = stopMoving, text='Stop' )

def printLineStats():
    print(f"LEFT: Start: {(start_width,start_Height)} END: {(end_width,end_Height)}",)
    print(f"RIGHT: Start: {(width // 2, 730)} END: {(width // 2, 770)}")
button( bind = printLineStats, text='PrintLineStats' )

# Left Line
value = 5
start_width = 380
end_width = 355
start_Height = 730
end_Height = 770

# warpAnglePerPixel = 0.168361861 # How much warping per pixel with given angle 
# warpAnglePerPixel = 0.151525675 # How much warping per pixel with given angle 
warpAnglePerPixel = 0.017 # How much warping per pixel with given angle 

def start_width_right():
    global start_width
    start_width += value
button( bind = start_width_right, text='StartWidthMoveRight' )

def start_width_left():
    global start_width
    start_width -= value
button( bind = start_width_left, text='StartWidthMoveLeft' )


def end_width_right():
    global end_width
    end_width += value
button( bind = end_width_right, text='EndWidthMoveRight' )

def end_width_left():
    global end_width
    end_width -= value
button( bind = end_width_left, text='EndWidthMoveLeft' )

def start_Height_right():
    global start_Height
    start_Height += value
button( bind = start_Height_right, text='StartHeightMoveDown' )

def start_Height_left():
    global start_Height
    start_Height -= value
button( bind = start_Height_left, text='StartHeightMoveDown' )

def end_Height_up():
    global end_Height
    end_Height -= value
button( bind = end_Height_up, text='EndHeightMoveUp' )

def end_Height_down():
    global end_Height
    end_Height += value
button( bind = end_Height_down, text='EndHeightMoveDown' )


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
        elif key.char == 'b':
            scene.center = batsmanFoot.pos
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
temp = 1

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    cv2.namedWindow("MainWindow", cv2.WINDOW_NORMAL)
    height, width, _ = frame.shape
    cv2.line(frame, (width // 2, 730), (width // 2, 770), (0, 0, 255), 5) # RIGHT LINE 
    cv2.line(frame, (start_width,start_Height),(end_width,end_Height),(0,0,255),5) # Left Line
    cv2.line(frame, (end_width,end_Height),(width // 2, 770),(255,0,0),5) # Line Joining 2 lines
    print(f"Window Size: {(height, width)}")
    
    #     # ((width // 2)-i) + start_width - ((width // 2)-i)
    #     # cv2.line(frame, (((width // 2)-i),start_Height),((width // 2)-i, 770),(0,255,0),5) # Line Joining 2 lines1
    #     angle = math.atan(968/i)
    #     radianAngle = math.radians(angle)
    #     distance = 40
    #     startX = i
    #     startY = 770
    #     endX = int(startX+distance*math.cos(radianAngle))
    #     endY = int(startY+distance*math.sin(radianAngle))
    #     print(startX,startY,endX,endY)

    #     cv2.line(frame, (startX,startY),(endX, endY),(0,255,0),5) # Line Joining 2 lines


    # cv2.resizeWindow("MainWindow", 800,600)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_pose.process(frame_rgb)
    landmarks = ''
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        if not initialFrameFlag:
            initX = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX].x
            initY = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX].y
            initialFrameFlag = 1
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        # print(f"\rFOOT COORDS {mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX}: {round(landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX].x,2)},{round(landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX].y,2)},{round(landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX].z,2)}", end='', flush=True)
        # Get the position of a specific landmark (e.g., RIGHT_FOOT_INDEX) & update the pose object's position in VPython
        batsmanFoot.pos = vector(-(17.68/2) * scale,
                                 0.4,
                                 (initX - landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX].x) * batsmanScale)
        # wideLineDistanceShift = batsmanFoot.pos.z - stump22.pos.z+stump22.radius
        # if(wideLineDistanceShift >= 0.43*scale):
        #     virtual_guide_line.pos.z = return_crease3.pos.z
        # elif(wideLineDistanceShift >= 0 and wideLineDistanceShift < 0.43*scale):
        #     virtual_guide_line.pos.z = 0.89 * scale + wideLineDistanceShift
        # if(virtual_guide_line.pos.z > return_crease3.pos.z): virtual_guide_line.pos.z = return_crease3.pos.z
        # print(f"\rwideLineDistanceShift: {wideLineDistanceShift} :batsmanFoot.pos: {batsmanFoot.pos}", end='', flush=True)
    lines=[]
    for i in range(10,605,15):
        # cv2.line(frame,(960-i,770),(960,int(i*math.tan(math.radians(warpAnglePerPixel*i)))),(0,255,0),5) 
        # print(f"\n======\nStart: {(960-i,770)}, End: {(960,int(i*math.tan(math.radians(warpAnglePerPixel*i))))},")
        # print(f"Angle(Deg): {warpAnglePerPixel*i}")
        # print(f"Angle(Rads): {math.radians(warpAnglePerPixel*i)}")
        # print(f"TanValue : {math.tan(math.radians(warpAnglePerPixel*i))}")

            # Define the starting point (center of the canvas)
        start_point = (960 - i, 770)

        # Define the angle of inclination in degrees
        angle = math.atan(968/i)
        # radianAngle = math.radians(angle)
        # print("================================================================")
        # print(angle)
        # print(start_point)
        # Define the distance (length of the line)
        distance = 40

        # Calculate the endpoint of the line
        # angle_radians = math.radians(angle)
        end_point_x = int(start_point[0] + distance * math.cos(angle))
        end_point_y = int(start_point[1] - distance * math.sin(angle))
        end_point = (end_point_x, end_point_y)
        lines.append((start_point,end_point))
        # print(end_point)
        cv2.line(frame,start_point,end_point,(0,255,0),5)

    # results = mp_pose.process(frame_rgb)
    # if results.pose_landmarks:
        # landmarks = results.pose_landmarks.landmark
    X_mp = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX].x
    X_mp = int(X_mp*frame.shape[1])
    Y_mp = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX].y
    Y_mp = int(Y_mp*frame.shape[0])
    # print(lines[:5])
    # print("\r",X_mp,Y_mp,end="")
    areas={}
    for i,line in enumerate(lines):
        point=(X_mp,Y_mp)
        line_start = line[0]
        line_end = line[1]

        
        # Check for intersection between the point and line
        # def check_intersection(point, line_start, line_end):
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end
         # Calculate the area of the triangle formed by the point and line segment
        area = abs(0.5 * (x1 * (y2 - y) + x2 * (y - y1) + x * (y1 - y2)))
        # Calculate the length of the line segment
        # line_length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        areas[i]=area

            
            # Check if the area is approximately zero (point lies on the line segment)
            # if np.isclose(area, 0.0) and 0 <= ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / (line_length ** 2) <= 1:
            #     return True
            # return False
    min_line_area_index=min(areas,key=areas.get)
    intersecting_line=lines[min_line_area_index]
    cv2.line(frame,intersecting_line[0],intersecting_line[1],(255,0,255),5)

    #pixels in the video frame
    distance_shifted_pixels=900-intersecting_line[0][0]
    print(distance_shifted_pixels)
    #1pixel in metres in the video frame
    pixel_scale=0.002237288
    distance_shifted_metres=distance_shifted_pixels*pixel_scale
    print(distance_shifted_metres)
    print("*"*100)
    if(distance_shifted_metres>=0.43):
        virtual_guide_line.pos.z = return_crease3.pos.z
    elif(distance_shifted_metres >= 0 and distance_shifted_metres < 0.43):
            virtual_guide_line.pos.z = 0.89 * scale + distance_shifted_metres*scale
    if(virtual_guide_line.pos.z > return_crease3.pos.z): virtual_guide_line.pos.z = return_crease3.pos.z
        # print(check_intersection(point, line_start, line_end))
        # Check for intersection
        # if check_intersection(point, line_start, line_end):
        #     # Intersection detected
            
        #     print(f"Intersection between the point {point} and line ({line_start},{line_end})")

    cv2.imshow('MainWindow', frame) 


    while temp:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            batsmanFoot.pos = vector(0,0,0)
            break

    if not temp and cv2.waitKey(1) & 0xFF == ord('q'):
        batsmanFoot.pos = vector(0,0,0)
        break
    
    # cv2.imshow('MainWindow', frame)

    # while temp:
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         batsmanFoot.pos = vector(0,0,0)
    #         break

    # if not temp and cv2.waitKey(1) & 0xFF == ord('q'):
    #     batsmanFoot.pos = vector(0,0,0)
    #     break
    # rate(60)

mp_pose.close()
cap.release()
cv2.destroyAllWindows()