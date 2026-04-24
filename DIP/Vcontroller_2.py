import cv2
import pyautogui
import numpy as np
import vgamepad as vg

gamepad = vg.VDS4Gamepad()  

width, height = pyautogui.size()

cam = cv2.VideoCapture(0)

def detect_green_in_roi(frame, x1, y1, x2, y2, threshold=1500):
    """Returns True if green color is detected in the given rectangle region."""
    # Ensure coordinates are ordered correctly
    rx1, rx2 = min(x1, x2), max(x1, x2)
    ry1, ry2 = min(y1, y2), max(y1, y2)

    roi = frame[ry1:ry2, rx1:rx2]

    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define green color range in HSV
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_pixels = cv2.countNonZero(mask)

    return green_pixels > threshold, green_pixels


def Jump():
    gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
    print("Jump")


def Attack():
    gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)
    print("Attack")


def Heal():
    gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
    print("Heal")


while True:
    suc, frame = cam.read()
    if not suc:
        break

    frame = cv2.resize(frame, (width, height))
    frame = cv2.flip(frame, 1)

    x1_L1 = 300
    x2_L1 = 100
    y1 = 300
    y2 = 800

    
    x1_R1 = 1100 + x1_L1
    x2_R1 = 1100 + x2_L1

    x1_R2 = x1_R1 + 220   
    x2_R2 = x2_R1 + 220   
    x1_L2 = x1_L1 + 300   
    x2_L2 = x2_L1 + 300

    x1_R2 = x1_R1 + 300   
    x2_R2 = x2_R1 + 300


    left_detected,  _ = detect_green_in_roi(frame, x1_L1, y1, x2_L1, y2)
    right_detected, _ = detect_green_in_roi(frame, x1_L2, y1, x2_L2, y2)

    y1_J_A=800
    y2_J_A=300
    jump_detected,  _ = detect_green_in_roi(frame, x1_R1, y1_J_A, x2_R1, y2_J_A)
    attack_detected,_ = detect_green_in_roi(frame, x1_R2, y1_J_A, x2_R2, y2_J_A)


    # UP button 
    x1_up=x1_L1-200
    x2_up=x2_L2+200
    y1_up=100
    y2_up=270
    Up_detected,_ = detect_green_in_roi(frame, x1_up, y1_up, x2_up, y2_up)

    # heal
    x1_heal=x1_up+1100
    x2_heal=x2_up+1100
    y1_heal=100
    y2_heal=270
    Heal_detected,_ = detect_green_in_roi(frame, x1_heal, y1_heal, x2_heal, y2_heal)


   
    if left_detected and not right_detected:
        x_val = -1.0
        print("Left")
    elif right_detected and not left_detected:
        x_val = 1.0
        print("Right")
    else:
        x_val = 0.0  # both or neither → neutral
    
    if Up_detected :
        y_val = -1.0
        print("UP")

    else:
        y_val = 0.0  # both or neither → neutral

    # --- Handle buttons ---
    if jump_detected:
        Jump()
    else:
        gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)

    if attack_detected:
        Attack()
        
    else:
        gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)
    
    if Heal_detected:
        Heal()

    else:
        gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)


    #one single update per frame 
    gamepad.left_joystick_float(x_value_float=x_val, y_value_float=y_val)
    gamepad.update()  


    
    color = (0, 255, 0) if Up_detected else (0, 0, 255)
    cv2.rectangle(frame,(x1_up,y1_up),(x2_up,y2_up),color,2)
    cv2.putText(frame, "Up", ((x1_up//2)+300, (y1_up//2)+150), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)



    # Left button
    color = (0, 255, 0) if left_detected else (0, 0, 255)
    cv2.rectangle(frame,(x1_L1,y1),(x2_L1,y2),color,2)
    cv2.putText(frame, "LEFT", ((x1_L1//2)+10, (y1//2)+400), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)


   


    # Right button
    color = (0, 255, 0) if right_detected else (0, 0, 255)
    cv2.rectangle(frame,(x1_L2,y1),(x2_L2,y2),color,2)
    cv2.putText(frame, "Right", ((x1_L2//2)+190, (y1//2)+400), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)


    
    
    # Jump button
    color = (0, 255, 0) if jump_detected else (0, 0, 255)
    cv2.rectangle(frame,(x1_R1,y1_J_A),(x2_R1,y2_J_A),color,2)
    cv2.putText(frame, "Jump", ((x2_R1//2)+650, (y1//2)+400), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)



    # Attack button
    color = (0, 255, 0) if attack_detected else (0, 0, 255)
    cv2.rectangle(frame,(x1_R2,y1_J_A),(x2_R2,y2_J_A),color,2)

    cv2.putText(frame, "Attack", ((x2_R1//2)+980, (y1//2)+400), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # print(detect_green_in_roi(frame,x1_L1,y1,x2_L1,y2))
  

    # Heal button
    color = (0, 255, 0) if Heal_detected else (0, 0, 255)
    cv2.rectangle(frame,(x1_heal,y1_heal),(x2_heal,y2_heal),color,2)
    cv2.putText(frame, "Heal", ((x2_heal//2)+580, (y1_up//2)+150), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("W", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
del gamepad

