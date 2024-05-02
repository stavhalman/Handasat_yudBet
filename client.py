import socket
import protocol
import cv2
import time
from ultralytics import YOLO


serverAddress = ('10.0.0.22',8888)

UDPClient=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
UDPClient.connect(serverAddress)
print("connected")
protocol.sendMessage("takePicture()","do",UDPClient)
protocol.sendMessage('sendMessage("Picture.png","picture",mySocket)',"do",UDPClient)
protocol.reciveMessage(UDPClient)
print("recived")

windowHight = 480
windowLength = 640
# load yolov8 model
model = YOLO('best.pt')

# load video
video_path = 'Picture.png'

frame = cv2.imread(video_path)

results = model.track(frame, persist=True, conf = 0.5, iou = 0.5)

frame_ = results[0].plot()

if results[0] != None:
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
time.sleep(10)
