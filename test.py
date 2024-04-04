
import cv2
  
cam_port = 0
cam = cv2.VideoCapture(cam_port) 
  
result, image = cam.read() 
  

if result: 

    cv2.imshow("GeeksForGeeks", image) 
  

    cv2.imwrite("Handasat_yudBetPicture.png", image) 
  
    cv2.waitKey(0) 
    cv2.destroyWindow("GeeksForGeeks") 

