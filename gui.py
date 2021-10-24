
import os
import cv2
from PIL import Image, ImageTk
import tkinter as tk
import mediapipe as mp
import numpy as np


class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        self.master = master
        self.frame2 = tk.Frame(master)
        self.label1 = tk.Label(self.frame2)
        self.label1.configure(activebackground='#8a9fb7', activeforeground='#8a9fb7', anchor='n', background='#8a9fb7')
        self.label1.configure(foreground='#c50106', highlightbackground='#fd4448', highlightcolor='#fd4448', justify='center')
        self.label1.configure(relief='ridge', text='SomeTextHere')
        self.label1.place(anchor='n', relx='0.5', x='0', y='0')
        self.button1 = tk.Button(self.frame2)
        self.button1.configure(activebackground='#0c5801', background='#09bd12', text='Start')
        self.button1.place(anchor='center', relwidth='0.2', relx='0.2', rely='0.91', x='0', y='0')
        self.button1.configure(command=self.startOpenCv)
        self.button2 = tk.Button(self.frame2)
        self.button2.configure(activebackground='#c65e00', background='#a7a41f', text='Reset')
        self.button2.place(anchor='center', relwidth='0.2', relx='0.5', rely='0.91', x='0', y='0')
        self.button2.configure(command=self.resetCount)
        self.button3 = tk.Button(self.frame2)
        self.button3.configure(activebackground='#df0005', background='#ff6266', text='End')
        self.button3.place(anchor='center', relwidth='0.2', relx='0.8', rely='0.91', x='0', y='0')
        self.button3.configure(command=self.quitEverything)
        self.frame2.configure(background='#8a9fb7', height='600', width='800')
        self.frame2.pack(side='top')
        self.lmain = tk.Label(master)
        self.lmain.pack()
        
        # Main widget
        self.mainwindow = self.frame2
        
        # opencv stuff
        self.width, self.height = 800, 600
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        # Non Gui stuff
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.count = 0
        self.heightToCross = 0.2 # as a factor of frameHeight from top of the frame

        self.heightToCrossOnTheWayUp = self.heightToCross*1.1
        self.heightToCrossOnTheWayDown = self.heightToCross*0.9
        self.handsAreUp = False

        # mediapipey stuff
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def show_frame(self):
        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        cv2image.flags.writeable = False
        results = self.pose.process(cv2image)
        if results.pose_landmarks is not None:
            for id, landmark in enumerate(results.pose_landmarks.landmark):
                if id ==15:
                    indX, indY = int(landmark.x*self.width), int(landmark.y*self.height)
                    cv2.circle(cv2image, (indX,indY),5,(255,0,0),2)
                    if indY < self.height*self.heightToCrossOnTheWayUp:
                        self.handsAreUp = True
                        cv2.circle(cv2image, (indX,indY),5,(0,255,0),2)
                    elif indY > self.height*self.heightToCrossOnTheWayDown and self.handsAreUp:
                        self.handsAreUp = False
                        self.count += 1
                        print(self.count)
        uB=0
        lB=self.height
        wide = 50
        countBar = np.interp(self.count,[0,30],[lB,uB])
        cv2.rectangle(cv2image, (self.width-wide, int(countBar)), (self.width, lB), (0, 0, 255), cv2.FILLED)
        cv2.rectangle(cv2image, (self.width-wide, uB), (self.width, lB), (255, 0, 0), 3)


        self.mp_drawing.draw_landmarks(
        cv2image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label1.imgtk = imgtk
        self.label1.configure(image=imgtk)
        self.label1.after(1, self.show_frame)
        # self.label1.after()
    def startOpenCv(self):
        self.show_frame()

    def resetCount(self):
        self.count = 0

    def quitEverything(self):
        self.cap.release()
        self.master.quit()

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = NewprojectApp(root)
    app.run()

