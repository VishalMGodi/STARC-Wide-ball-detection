from vpython import *
from pynput import keyboard, mouse
from win32api import GetSystemMetrics

# Get Computer Screen width and height
scene.width = GetSystemMetrics(0) - GetSystemMetrics(0)/10
scene.height = GetSystemMetrics(1) - GetSystemMetrics(1)/4

scale = 100 # 1 meter = 100 pixels
camera_speed = 20


# CAMERA CONSTANTS
CAMERA_X, CAMERA_Y, CAMERA_Z = 1381.57, 98.7792, -60.0066
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

# Initialize the camera
scene.camera.pos = initial_camera_pos
centerBall = sphere(pos = cameraCenter,radius = 0.1*scale, color = color.red)
# scene.autoscale = False
scene.center = initial_camera_pos

# Move the camera on WASD keys
def keyInput(key):
	camera_x = scene.camera.pos.x
	camera_y = scene.camera.pos.y
	camera_z = scene.camera.pos.z

	try:
		if key.char == "w":
			camera_z -= 1 * camera_speed
		elif key.char == 's':
			camera_z += 1 * camera_speed
		elif key.char == 'a':
			camera_x -= 1 * camera_speed
		elif key.char == 'd':
			camera_x += 1 * camera_speed
		elif key.char == 'r':
			scene.center = centerBall.pos
			return
	except AttributeError:
		if key == keyboard.Key.space:
			camera_y += 1 * camera_speed
		elif key == keyboard.Key.shift:
			camera_y -= 1 * camera_speed
	camera_pos_rel = vector(camera_x,camera_y,camera_z) - cameraCenter
	scene.camera.pos = camera_pos_rel + cameraCenter


listener = keyboard.Listener(on_press=keyInput)
listener.start()

while True:
	rate(30)

