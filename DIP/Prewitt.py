import cv2 
import numpy as np

def Prewitt(image):
    img=cv2.imread(image)

    kernal_x=np.array([[-1,0,1],
                    [-1,0,1],
                    [-1,0,1]])

    Prewitt_x=cv2.filter2D(img,-1,kernal_x)
    
    kernal_y=np.array([[1,1,1],
                    [0,0,0],
                    [-1,-1,-1]])

    Prewitt_y=cv2.filter2D(img,-1,kernal_y)

    Prewitt_combined=Prewitt_x+Prewitt_y



    cv2.imwrite("Prewitt_x.png",Prewitt_x)
    cv2.imwrite("Prewitt_y.png",Prewitt_y)
    cv2.imwrite("Prewitt_Combined.png",Prewitt_combined)

    cv2.imshow("Prewitt x",Prewitt_x)
    cv2.imshow("Prewitt y",Prewitt_y)
    cv2.imshow("Prewitt Combined",Prewitt_combined)
    cv2.waitKey(0)

Prewitt("Test.png")

