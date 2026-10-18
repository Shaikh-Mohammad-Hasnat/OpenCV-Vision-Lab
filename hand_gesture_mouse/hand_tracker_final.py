import cv2
import time as tm
import numpy as np
import pyautogui
import mediapipe as mp
import collections


# ---------------- CONFIG ----------------
SMOOTHING_POINTS = 7
# distance threshold (pixels) to consider fingers "pinched"
CLICK_THRESHOLD = 20
RING_CLICK_THRESHOLD = 20
# time (seconds) a pinch must be held to start drag
DRAG_HOLD_TIME = 0.6
# minimum time between clicks
CLICK_COOLDOWN = 0.4
MOVE_SCALE = 6
# ----------------------------------------


pyautogui.FAILSAFE = False
points = collections.deque(maxlen=SMOOTHING_POINTS)

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

is_dragging = False
gesture_active = False
last_gesture_time = 0
pinch_start_time = 0

while True:
    ptime = tm.time()
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)

    index = thumb = middle = None
    first_click=second_click = None

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            # --------- LANDMARK EXTRACTION ---------
            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8:
                    index = (cx, cy)
                    cv2.circle(img, index, 10, (255, 0, 255), cv2.FILLED)

                elif id == 4:
                    thumb = (cx, cy)
                    cv2.circle(img, thumb, 10, (0, 255, 0), cv2.FILLED)

                elif id == 12:
                    middle = (cx, cy)
                    cv2.circle(img, middle, 10, (0, 0, 255), cv2.FILLED)
                elif id == 16:
                    ring = (cx, cy)
                    cv2.circle(img, ring, 10, (255, 255, 0), cv2.FILLED)

            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

            # --------- MOUSE MOVE ---------
            if index:
                points.append(index)
                avg_x = int(sum(p[0] for p in points) / len(points))
                avg_y = int(sum(p[1] for p in points) / len(points))
                pyautogui.moveTo(avg_x * MOVE_SCALE, avg_y * MOVE_SCALE, duration=0.01)

            # --------- GESTURE / DRAG ---------
            current_time = tm.time()

            # Right click: thumb + ring
            if thumb and ring:
                dist_tr = np.linalg.norm(np.array(thumb) - np.array(ring))
                if dist_tr < RING_CLICK_THRESHOLD and (current_time - last_gesture_time) > CLICK_COOLDOWN:
                    pyautogui.click(button="right")
                    print("RIGHT CLICK (thumb + ring)")
                    last_gesture_time = current_time

            # Left click or drag: thumb + middle
            if thumb and middle:
                dist_tm = np.linalg.norm(np.array(thumb) - np.array(middle))

                # Pinch detected
                if dist_tm < CLICK_THRESHOLD:
                    if not gesture_active:
                        gesture_active = True
                        pinch_start_time = current_time
                    # If held long enough, start dragging
                    if (current_time - pinch_start_time) >= DRAG_HOLD_TIME and not is_dragging:
                        is_dragging = True
                        pyautogui.mouseDown(button='left')
                        print("DRAG STARTED")
                else:
                    # Pinch released
                    if gesture_active:
                        # short pinch -> left click
                        if not is_dragging and (current_time - pinch_start_time) < DRAG_HOLD_TIME and (current_time - last_gesture_time) > CLICK_COOLDOWN:
                            pyautogui.click(button="left")
                            print("LEFT CLICK (thumb + middle)")
                            last_gesture_time = current_time
                        # end drag if it was active
                        if is_dragging:
                            pyautogui.mouseUp()
                            is_dragging = False
                            print("DRAG ENDED")
                    gesture_active = False

            # If dragging, move mouse with smoothed index position
            if is_dragging and index:
                avg_x = int(sum(p[0] for p in points) / len(points))
                avg_y = int(sum(p[1] for p in points) / len(points))
                pyautogui.moveTo(avg_x * MOVE_SCALE, avg_y * MOVE_SCALE, duration=0.01)

    # --------- FPS ---------
    ctime = tm.time()
    fps = 1 / (ctime - ptime)
    cv2.putText(img, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Mouse Control", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()