import cv2
import mediapipe as mp
import time
import math
from pynput.mouse import Button, Controller
import ctypes
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

mouse = Controller()

user32 = ctypes.windll.user32
W, H = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

pTime = 0
with mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        success, image = cap.read()
        # image = cv2.flip(image,1)
        cTime = time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        
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
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        h,w,c = image.shape
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                for id, lm in enumerate(hand_landmarks.landmark):
                    if id == 4:
                        indX, indY = int(lm.x*w), int(lm.y*h)
                        cv2.circle(image, (indX,indY),5,(255,0,0),2)
                    elif id ==8:
                        thumbX, thumbY = int(lm.x*w), int(lm.y*h)
                        cv2.circle(image, (thumbX,thumbY),5,(255,0,0),2)
                        
                if indX and indY and thumbX and thumbY:
                    cv2.line(image,(indX,indY),(thumbX,thumbY),(255,0,0),2)
                    cx, cy = (indX+thumbX)//2, (indY+thumbY)//2
                    cv2.circle(image, (cx,cy),8,(255,0,0),1)
                    length = math.hypot(thumbX-indX,thumbY-indY)
                    
                    posx, posy = np.interp(cx,[0,w],[0,W]), np.interp(cy,[0,h],[0,H])
                    # print('cx: %d, cy: %d, posx: %d, posy: %d'%(cx,cy,posx,posy))
                    mouse.position = (posx,posy)
                    
                    if length < 50:
                        mouse.press(Button.left)
                    elif length > 50:
                        mouse.release(Button.left)
        cv2.putText(image, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
        cv2.imshow('MediaPipe Hands', image)
        
        if cv2.waitKey(1) & 0xFF == 27:
          break
cap.release()