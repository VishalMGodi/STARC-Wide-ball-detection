#########################
# Client recieving imgs #
#########################

import socket, cv2, pickle, struct

import numpy as np
fps, seconds, minutes = 60, 60, 2
total_frames = fps*seconds*minutes
Video1 = np.array(total_frames)

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '10.14.142.231'#'192.168.1.20'  # paste your server ip address here
port = 9999
client_socket.connect((host_ip, port))  # a tuple
data = b""
payload_size = struct.calcsize("QQ")
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # 4K
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size, i = struct.unpack("QQ", packed_msg_size)

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("RECEIVING VIDEO", frame)
    if cv2.waitKey(1) == '13':
        break
client_socket.close()


#######################
# server sending imgs #
#######################

import socket, cv2, pickle, struct, imutils

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)
fps, seconds, minutes = 60, 60, 2
total_frames = fps*seconds*minutes
# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        i=0
        while (vid.isOpened()):
            i%= total_frames #fps*s*m
            img, frame = vid.read()
            print(frame.shape)
            # input()
            # frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("QQ", len(a), i) + a
            client_socket.sendall(message)

            cv2.imshow('TRANSMITTING VIDEO', frame)
            if cv2.waitKey(1) == '13':
                client_socket.close()
            i+=1
