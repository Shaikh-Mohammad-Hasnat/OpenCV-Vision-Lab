import cv2
import numpy as np

def Laplacian(image):

   
    kernal=np.array([[0,-1,0],
                    [-1,4,-1],
                    [0,-1,0]])

    lap_image=cv2.filter2D(image,-1,kernal)

    return lap_image

def Sobel(image):
    

    kernal_x=np.array([[-1,0,1],
                    [-2,0,2],
                    [-1,0,1]])

    Sobel_image_x=cv2.filter2D(image,-1,kernal_x)
    
    kernal_y=np.array([[1,2,1],
                    [0,0,0],
                    [-1,-2,-1]])

    Sobel_image_y=cv2.filter2D(image,-1,kernal_y)

    return Sobel_image_x+Sobel_image_y



def Prewitt(image):


    kernal_x=np.array([[-1,0,1],
                    [-1,0,1],
                    [-1,0,1]])

    Prewitt_x=cv2.filter2D(image,-1,kernal_x)
    
    kernal_y=np.array([[1,1,1],
                    [0,0,0],
                    [-1,-1,-1]])

    Prewitt_y=cv2.filter2D(image,-1,kernal_y)

    return cv2.add(Prewitt_x,Prewitt_y)




  
cam=cv2.VideoCapture(0)

while True:
    suc,frame=cam.read()
    if not suc:
        break
    frame=cv2.resize(cv2.cvtColor(cv2.flip(frame,1),cv2.COLOR_BGR2GRAY),(500,500))
    
    cv2.imshow("Laplacian",Laplacian(frame))
    cv2.imshow("Sobel",Sobel(frame))
    cv2.imshow("Prewitt",Prewitt(frame))
    cv2.waitKey(1)