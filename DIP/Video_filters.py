import cv2
import numpy as np
import random
cam=cv2.VideoCapture(0)

def neagtive(frame):
    New_frame=255-frame
    cv2.imshow("negative",New_frame)

def thresholding(frame,threshold_value):
    ret,thresh=cv2.threshold(frame,threshold_value,255,cv2.THRESH_BINARY)
    cv2.imshow("thresholding",thresh)

def Contrast_stretching(frame):
    r_min=np.min(frame)

    r_max=np.max(frame)

    cotrast_stretcched=((frame-r_min)/(r_max-r_min))*255

    contrast_stretcched=cotrast_stretcched.astype(np.uint8)
    contrast_stretcched=cv2.cvtColor(contrast_stretcched, cv2.COLOR_GRAY2RGB)
    cv2.imshow("Contrast Stretching",contrast_stretcched)
    

def laplacian(frame):
   
    kernel=np.array([[0,-1,0],
                    [-1,4,-1],
                    [0,-1,0]])

    cv2.imshow("Laplacian",cv2.filter2D(frame,-1,kernel))

def laplacian_composite(frame):
   
    kernel=np.array([[0,-1,0],
                    [-1,5,-1],
                    [0,-1,0]])
    
    

    cv2.imshow("composite Laplacian",cv2.filter2D(frame,-1,kernel))

def noise(frame, probability=0.02):

    height, width = frame.shape
    New_frame=frame.copy()
    for i in range(height):
        for j in range(width):

            r = random.random()   # random number 0–1

            if r < probability:
                
                        New_frame[i][j]= 255   # white noise

        cv2.imshow("Noise", New_frame)

def equalize_histogram(frame):
    equalized_image = cv2.equalizeHist(frame)

    cv2.imshow('Equalized Image (HE)', equalized_image)
    
def Flip_add(frame):

    flip=cv2.flip(frame,0)

    cv2.imshow("Flip Added",frame+flip)


while True:
    suc,frame=cam.read()
    if not suc:
        print("Failed to grab frame")
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame=cv2.flip(frame,1) 
    frame=cv2.resize(frame,(300,300))

    cv2.imshow("cam",frame)
    neagtive(frame)
    thresholding(frame,125)
    Contrast_stretching(frame)
    laplacian(frame)
    laplacian_composite(frame)
    noise(frame)
    equalize_histogram(frame)
    Flip_add(frame)

    if cv2.waitKey(1) == 27:  # press ESC to exit
     break

cam.release()
cv2.destroyAllWindows()