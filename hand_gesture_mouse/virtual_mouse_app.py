import mediapipe as mp
import cv2 as cv2
# import numpy as np
import pyautogui as pg
import os

pg.FAILSAFE = False
cap = cv2.VideoCapture(0)

while True:

    thumb = middle = ring = None
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)
    result = hands.process(imgRGB)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    try:
        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                for id, lm in enumerate(hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    if id == 8:
                        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                        thumb = (cx, cy)
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        pg.moveTo(abs(cx * 6), abs(cy * 6))
                        
                    elif id == 4:
                        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                        thumb = (cx, cy)    

                    elif id == 12:
                        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                        middle = (cx, cy)
                    
                    if(thumb and middle):
                        if(abs(thumb[0]-middle[0])>=0):
                            print("left")
                    #     dist_thumb_middle = np.linalg.norm(np.array(thumb) - np.array(middle))

                    #     if dist_thumb_middle < 40:
                    #         pg.click(button="left")
                    #         cv2.circle(img, thumb, 15, (0, 255, 255), cv2.FILLED)

                mp_draw = mp.solutions.drawing_utils
                mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)


        cv2.imshow("Image", img)
        cv2.waitKey(1)

    except Exception as e:
        # print(e)
        pass
cv2.destroyAllWindows()
cap.release()