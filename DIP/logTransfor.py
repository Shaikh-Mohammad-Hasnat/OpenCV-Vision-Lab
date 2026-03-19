import cv2
import numpy as np

def LogTrasnform(frame):
    frame_float = frame.astype(np.float32)
    # Apply log transform using OpenCV
    c = 255 / (np.log(1 + np.max(frame_float)))
    log_transformed = c * np.log(1 + frame_float)
    log_transformed = np.array(log_transformed, dtype = np.uint8) # Convert back to uint8
    
    return log_transformed


cam=cv2.VideoCapture(0)
while True:
    suc,frame=cam.read()
    if not suc:
        break

    cv2.imshow("LogTransformation",cv2.flip(LogTrasnform(frame),1))
    cv2.waitKey(1)
cv2.destroyAllWindows()