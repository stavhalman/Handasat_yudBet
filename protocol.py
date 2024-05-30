import socket
import cv2
from ultralytics import YOLO
import pygame
import classes
import time

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
        messageLength = str(len(message)//1024+1)

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
    if( messageType != "ok"):
        print("sent")
        reciveMessage(mySocket)
        print("confirmed")

#recive a socket and recive a message from it, acts acording to message type
def reciveMessage(mySocket:socket.socket):

    #get socket type length
    messageTypeLength:int = int(mySocket.recv(1).decode())
    print(messageTypeLength)

    #get the socket type
    messageType = mySocket.recv(messageTypeLength).decode()   
    print(messageType) 
    

    if messageType == "do":

        #get command
        message = mySocket.recv(1024).decode()

        print("recived")
        sendMessage("","ok",mySocket)
        print("sent confirmation")

        #do command
        print("doing: "+message)
        eval(message)

    
    elif messageType == "picture":

        #def a bytes veriable
        data:bytes = b''

        #recive all the bytes of the picture
        length = int(mySocket.recv(6))
        print(length)
        for i in range(length):   
            print(i)
            data += mySocket.recv(1024)

        #save picture
        with open ('Picture.png','wb') as file:
            file.write(data)

        print("recived")
        sendMessage("","ok",mySocket)
        print("sent confirmation")       
        
    

def showPicture(screen):
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


def button(x,y,w,h,buttonText,screen, action):
    font = pygame.font.SysFont('freesanbold.ttf', 50)
    text = font.render(buttonText, True, (255, 255, 255))
    textRect1 = text.get_rect()
    textRect1.center = (x+w/2, y+h/2)
    pygame.draw.rect(screen,(255,255,255),[x,y,w,h],5)
    screen.blit(text, textRect1)

def refresh(UDPClient,screen):
    print("1")
    sendMessage("takePicture()","do",UDPClient)
    print("2")
    sendMessage('sendMessage("Picture.png","picture",mySocket)',"do",UDPClient)
    print("3")
    reciveMessage(UDPClient)
    print("4")
    showPicture(screen)  
    print("5")
    screen.blit(pygame.image.load('AfterCode.png'), (0, 0))
    print("6")
    pygame.display.flip()
    print("7")

def select(results):
    while pygame.event.get().type != pygame.MOUSEBUTTONUP:
        pass
    while pygame.event.get().type != pygame.MOUSEBUTTONDOWN:
        pass
    for box in results[0].boxes:
        if box.xyxy[0][0] < pygame.mouse.get_pos()[0] and box.xyxy[0][2] > pygame.mouse.get_pos()[0] and box.xyxy[1][0] < pygame.mouse.get_pos()[1] and box.xyxy[1][2] > pygame.mouse.get_pos()[1]:
            return box

def setUp():
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1030
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Project")

    screen.blit(pygame.image.load('AfterCode.png'), (0, 0))

    return screen