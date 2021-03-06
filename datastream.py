import json
import cv2
import mediapipe as mp
import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

server_address = (local_ip, 10000)
#print(server_address)
sock.bind(server_address)



print("\n\n\n\n\n\n\n\n\n\n\n\n\nUse this ip to connect to Model Renderer!\n")
print(local_ip)

ip = False


while ip is False:
    print('waiting to receive message')
    data, address = sock.recvfrom(4096)
    
    print ('received ' + str(len(data)) + ' bytes from ' + str(address))
    print(data)
    
    if data:
        sent = sock.sendto(data, address)
        print('sent ' + str(sent) + ' bytes back to ' + str(address))
        ip = address

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

print(mp_pose)

mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

#path_to_file = "unity/renderer/Assets"

# For webcam input:
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

pose = mp_pose.Pose(min_detection_confidence=0.6,
                    min_tracking_confidence=0.6,
                    model_complexity=2)

hands = mp_hands.Hands(min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)
    
imgs = 0
lastsec = round(time.time()) % 10
sec = lastsec

print("")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = pose.process(image)
    results2 = hands.process(image)
    results3 = face_mesh.process(image)
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #print(results.pose_landmarks.SerializeToString())

    mp_drawing.draw_landmarks(image, results.pose_landmarks,
                              mp_pose.POSE_CONNECTIONS)

    poseData = []
    if results.pose_landmarks:
        for data_point in results.pose_landmarks.landmark:
            poseData.append({
                'x': data_point.x,
                'y': data_point.y,
                'z': data_point.z,
                'visibility': data_point.visibility,
            })
        #print(poseData)

    handData = []
    if results2.multi_hand_landmarks:
        #print(results2.multi_hand_landmarks)

        for hand_landmarks in results2.multi_hand_landmarks:
            for data_point in hand_landmarks.landmark:
                handData.append({
                    'x': data_point.x,
                    'y': data_point.y,
                    'z': data_point.z,
                })
            mp_drawing.draw_landmarks(image, hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS)

    #print(handData)

    faceData = []
    if results3.multi_face_landmarks:
        #print(results3.multi_face_landmarks)
        for face_landmarks in results3.multi_face_landmarks:
            for data_point in face_landmarks.landmark:
                faceData.append({
                    'x': data_point.x,
                    'y': data_point.y,
                    'z': data_point.z,
                })
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACE_CONNECTIONS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec)

    #cv2.imshow('MediaPipe Model', image)

    data = json.dumps({'pose': poseData, 'hands': handData, 'face': faceData})
    sock.sendto(bytearray(data, 'utf-8'), ip)
    
    sec = round(time.time()) % 10
    imgs+=1
    if sec != lastsec:
        lastsec = sec
        sys.stdout.write("\r" + str(imgs) + " updates/second!           ")
        sys.stdout.flush()
        imgs = 0

    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()