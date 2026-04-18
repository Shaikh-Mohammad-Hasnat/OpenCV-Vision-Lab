import cv2
import numpy as np

cam = cv2.VideoCapture("CCTVfootage.mp4")

def FrameCheck(Prev_frame, Curr_frame):
    Diff = cv2.absdiff(Prev_frame, Curr_frame)
    # Diff = cv2.resize(Diff,(200,200))

    _, thresh = cv2.threshold(Diff, 10, 255, cv2.THRESH_BINARY)
    motion_pixels = np.count_nonzero(thresh)
    return (Diff, thresh, motion_pixels)

ret, first_frame = cam.read()
Prev_frame = cv2.cvtColor(cv2.flip(first_frame, 1), cv2.COLOR_BGR2GRAY)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    Current_frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2GRAY)
    display_frame = cv2.flip(frame, 1)

    Diff, thresh, motion_pixels = FrameCheck(Prev_frame, Current_frame)

    if motion_pixels > 1500:
        print("\033[31mMOTION DETECTED\033[0m")
       
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 4)

        
        cv2.putText(display_frame, "Motion Detected", (30, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
    else:
    
        print("\033[32mNO MOTION DETECTED\033[0m")
    cv2.imshow("Diff", cv2.resize(Diff, (500, 450)))
    cv2.imshow("Motion Detection", cv2.resize(cv2.cvtColor(display_frame, cv2.COLOR_BGR2GRAY), (500, 450)))  #  one window shows both boxes + text
    cv2.imshow("Thre", cv2.resize(thresh, (500, 450)))  #  one window shows both boxes + text

    Prev_frame = Current_frame

    if cv2.waitKey(1) & 0xFF == ord('q'):  #  press Q to quit
        break

cam.release()
cv2.destroyAllWindows()