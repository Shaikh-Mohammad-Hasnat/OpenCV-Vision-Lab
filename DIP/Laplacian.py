import cv2 
import numpy as np

def Laplacian(image):
    img=cv2.imread(image)

    kernal=np.array([[0,-1,0],
                    [-1,4,-1],
                    [0,-1,0]])

    lap_image=cv2.filter2D(img,-1,kernal)

    cv2.imshow("W",lap_image)
    cv2.imwrite("Laplacian.png",lap_image)

    cv2.waitKey(0)

Laplacian("Test.png")

