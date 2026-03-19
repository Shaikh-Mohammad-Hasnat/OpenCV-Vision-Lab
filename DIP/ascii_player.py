"""
Steps  To Convert the image to ascii
1)open the video
2)convert the video to grayscale and resize it
3)make a blank canvas
4)Traverse the image using for loop
5)Get the brightness/intensity
6)calculate the char on index 
7)Put text at that value of image x,y

cv2.putText(img, 
            text, 
            org, 
            fontFace, 
            fontScale, 
            color, 
            thickness, 
            lineType, 
            bottomLeftOrigin)
"""
import cv2
import numpy as np


#path of the video

chars = "  .'`^\",:;Il!i><~+_-?][}{1)(|\\/*#ht&8%B@$"
cam=cv2.VideoCapture("video.mp4")
scale=10
while True:
    suc,frame=cam.read()

    if not suc:
        break

    #converts the image to grayscale    
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    #resize the image/video
    small=cv2.flip(cv2.resize(frame,(180,140)),1)

    #dimensions of the frame
    height,width=small.shape

    #drawing blnak canvas
    canvas=np.zeros((height*scale,width*scale,3),dtype=np.uint8)

    #Traverse the image
    for i in range(height):
        for j in range(width):
            #Get the intensity of pixel
            intensity=int(small[i][j])

            #Get the char index
            char_index=int(intensity/255*(len(chars)-1))

            char=chars[char_index]

            #put the text at given coordinates

            cv2.putText(canvas,
                        char,
                        (j*scale,i*scale),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        .3,
                        (255,255,0),
                        1)
    #Show the out put image
    cv2.imshow("Ascii Player",canvas)
    cv2.waitKey(1)
cam.release()  
cv2.destroyAllWindows()