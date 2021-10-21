import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
count = 0
heightToCross = 0.2 # as a factor of frameHeight from top of the frame

heightToCrossOnTheWayUp = heightToCross*1.1
heightToCrossOnTheWayDown = heightToCross*0.9
handsAreUp = False
# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        h,w,c = image.shape
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        for id, landmark in enumerate(results.pose_landmarks.landmark):
            if id ==15:
                indX, indY = int(landmark.x*w), int(landmark.y*h)
                cv2.circle(image, (indX,indY),5,(255,0,0),2)
                if indY < h*heightToCrossOnTheWayUp:
                    handsAreUp = True
                elif indY > h*heightToCrossOnTheWayDown and handsAreUp:
                    handsAreUp = False
                    count += 1
                    print(count)
        
        uB=0
        lB=h
        wide = 50
        countBar = np.interp(count,[0,30],[lB,uB])
        # cv2.rectangle(image, (0, int(F)), (wide, lB), (255, 0, 0), cv2.FILLED)
        # cv2.rectangle(image, (0, uB), (wide, lB), (0, 0, 255), 3)

        cv2.rectangle(image, (w-wide, int(countBar)), (w, lB), (0, 0, 255), cv2.FILLED)
        cv2.rectangle(image, (w-wide, uB), (w, lB), (255, 0, 0), 3)
        mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
        cv2.imshow('MediaPipe Pose', image)
        # cap.release()
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()