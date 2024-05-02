import socket
import cv2
from ultralytics import YOLO

def takePicture():

    #select camera
    cam_port = 0

    #get camera
    cam = cv2.VideoCapture(cam_port) 
    
    #get picture
    result, image = cam.read() 
    
    #if took picture
    if result: 
        #save picture
        cv2.imwrite("Picture.png", image) 

def moveTo(x,y):
    print("Move to ",x," ",y)

def select():
    print("Select")

#recive a message (string), message type (string) and socket. sends message to socket
def sendMessage(message:str,messageType,mySocket:socket.socket):

    #get socket type length
    messageTypeLength = str(len(messageType))

    if(messageType=="picture"):

        #get message from file
        with open (message,'rb') as file:
            message=file.read()

        #get message length
        messageLength = str(len(message)-7-len(messageType)//1024+1)

        #change messageLength to correct format
        messageLength = "0"*(6-len(messageLength))+messageLength

        #constract the start of the message by order
        start = messageTypeLength+messageType+messageLength

        #encode the start of the messsage
        start = start.encode()

        #send the start of the message
        mySocket.send(start)
    else:

        #constract message by order
        message = messageTypeLength+messageType+message

        #encode message
        message = message.encode()
    
    #send message
    mySocket.send(message)

#recive a socket and recive a message from it, acts acording to message type
def reciveMessage(mySocket:socket.socket):

    #get socket type length
    messageTypeLength:int = int(mySocket.recv(1).decode())

    #get the socket type
    messageType = mySocket.recv(messageTypeLength).decode()    

    if messageType == "do":

        #get command
        message = mySocket.recv(1024).decode()

        #do command
        eval(message)
    
    elif messageType == "picture":

        #def a bytes veriable
        data:bytes = b''

        #recive all the bytes of the picture
        for i in range(int(mySocket.recv(6))):   
            data += mySocket.recv(1024)

        #save picture
        with open ('Picture.png','wb') as file:
            file.write(data)

def showPicture():
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

    # visualize
    cv2.imshow('frame', frame_)

    #save picture
    cv2.imwrite("AfterCode.png", frame_)
    while True:
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

