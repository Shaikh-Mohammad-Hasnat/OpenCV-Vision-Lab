import cv2 
import numpy as np

def Sobel(image):
    img=cv2.imread(image)

    kernal_x=np.array([[-1,0,1],
                    [-2,0,2],
                    [-1,0,1]])

    Sobel_image_x=cv2.filter2D(img,-1,kernal_x)
    
    kernal_y=np.array([[1,2,1],
                    [0,0,0],
                    [-1,-2,-1]])

    Sobel_image_y=cv2.filter2D(img,-1,kernal_y)

    Sobel_combined=Sobel_image_x+Sobel_image_y



    # cv2.imwrite("Sobel_x.png",Sobel_image_x)
    # cv2.imwrite("Sobel_y.png",Sobel_image_y)
    # cv2.imwrite("Sobel_Combined.png",Sobel_combined)

    cv2.imshow("Sobel x",Sobel_image_x)
    cv2.imshow("Sobel y",Sobel_image_y)
    cv2.imshow("Sobel Combined",Sobel_combined)
    cv2.waitKey(0)

Sobel("Test.png")

