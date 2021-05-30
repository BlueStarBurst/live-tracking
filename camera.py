import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# For webcam input:
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

pose = mp_pose.Pose(min_detection_confidence=0.6,
                    min_tracking_confidence=0.6,
                    model_complexity=2)

hands = mp_hands.Hands(min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

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
    mp_drawing.draw_landmarks(image, results.pose_landmarks,
                              mp_pose.POSE_CONNECTIONS)
    if results2.multi_hand_landmarks:
        for hand_landmarks in results2.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS)

    if results3.multi_face_landmarks:
      for face_landmarks in results3.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACE_CONNECTIONS,
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=drawing_spec)

    cv2.imshow('MediaPipe Model', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()