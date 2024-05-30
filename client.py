import socket
import protocol
import cv2
import time
from ultralytics import YOLO

serverAddress = ('127.0.0.1',8888)
#10.0.0.22

UDPClient=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
UDPClient.connect(serverAddress)
print("connected")
protocol.sendMessage("takePicture()","do",UDPClient)
protocol.sendMessage('sendMessage("Picture.png","picture",mySocket)',"do",UDPClient)
protocol.reciveMessage(UDPClient)
print("done")

windowHight = 480
windowLength = 640
# load yolov8 model
model = YOLO('best.pt')
# load video
video_path = 'Picture.png'

frame = cv2.imread(video_path)

results = model.track(frame, persist=True, conf = 0.5, iou = 0.5)

frame_ = results[0].plot()

if len(results[0].boxes) > 0:
    highest = results[0].boxes[0]
    if(len(results[0].boxes) != 0):
        for bx in results[0].boxes:
            if bx.conf > highest.conf:
                highest = bx
        print(highest.conf)
        bouldingBoxMiddle = (highest.xyxy[0][0] + highest.xyxy[0][2])/2
        if(bouldingBoxMiddle<=windowLength/3):
            print("right")
        if(bouldingBoxMiddle>windowLength/3 and bouldingBoxMiddle<windowLength/3*2):
            print("middle")
        if(bouldingBoxMiddle<=windowLength and bouldingBoxMiddle>=windowLength/3*2):
            print("left")
    else:
        print("empty")
    
    #save picture
    cv2.imwrite("AfterCode.png", frame_)

    cv2.imshow("frame",frame_)
else:
    print("else")
    cv2.imshow("Picture.png",cv2.imread(video_path))

# waits for user to press any key 
# (this is necessary to avoid Python kernel form crashing) 
cv2.waitKey(0) 
  
# closing all open windows 
cv2.destroyAllWindows() 

print("done")