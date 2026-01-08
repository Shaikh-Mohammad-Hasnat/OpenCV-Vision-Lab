import cv2
import time as tm
import numpy as np
import pyautogui
import mediapipe as mp
import collections


# store last 5 points
points = collections.deque(maxlen=7)
pyautogui.FAILSAFE=False


cap= cv2.VideoCapture(0)
mphands=mp.solutions.hands
hands=mphands.Hands()
mpdraw=mp.solutions.drawing_utils

while True:

    ptime=tm.time()
    success,img=cap.read()
    img = cv2.flip(img, 1)  # Mirror image
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    index = None
    thumb = None
    middle = None
    cv2.waitKey(1)

    result=hands.process(imgRGB)
    # print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            for id,lm in enumerate(hand.landmark):
                # print(id,lm)
                h,w,l=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                if(id==8):
                    cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
                    index=(cx,cy)
                    # print(id,cx,cy)

                elif(id==4):
                    cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
                    thumb=(cx,cy)
                    # print(id,cx,cy)

                elif(id==12):
                    cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
                    middle=(cx,cy)
                    # print(id,cx,cy)
                
            mpdraw.draw_landmarks(img,hand,mphands.HAND_CONNECTIONS)     
            points.append(index)  # save the new point
            avg_x = int(sum(p[0] for p in points) / len(points))
            avg_y = int(sum(p[1] for p in points) / len(points))

            dist_thumb_middle = np.linalg.norm(np.array(thumb) - np.array(middle))

            dist_index_middle = np.linalg.norm(np.array(index) - np.array(middle))

            if thumb and middle and index:
                dist_thumb_middle = np.linalg.norm(np.array(thumb) - np.array(middle))
                dist_index_middle = np.linalg.norm(np.array(index) - np.array(middle))

              
                if dist_thumb_middle < 25:
                        pyautogui.click(button="right")
                        print("RIGHT CLICK")
                        tm.sleep(.1)

                
                if dist_index_middle < 25:
                    pyautogui.click(button="left")
                    print("LEFT CLICK")
                    tm.sleep(.1)


            pyautogui.moveTo(x=avg_x*7, y=avg_y*7)

    ctime=tm.time()
    fps=1/(ctime-ptime)
    cv2.putText(img,f"FPS:{int(fps)}",(10,25), cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 255, 0), 2)

    cv2.imshow("Image",img)
    cv2.waitKey(1)