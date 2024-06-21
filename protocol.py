import socket
import cv2
from ultralytics import YOLO
import pygame
import Classes
import time

#takes a picture and saves it
def take_picture():

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

#recives cordinations and activate the engines acordingly
def move_to(x,y):
    print("Move to ",x," ",y)

#recive a message (string), message type (string) and socket. sends message to socket
def send_message(message:str,messageType,mySocket:socket.socket):

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
        receive_message(mySocket)
        print("confirmed")

#recive a socket and recive a message from it, acts acording to message type
def receive_message(mySocket:socket.socket):

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
        send_message("","ok",mySocket)
        print("sent confirmation")

        #do command
        print("doing: "+message)
        eval(message)

    
    elif messageType == "picture":

        #def a bytes veriable
        data:bytes = b''

        #recive all the bytes of the picture
        length = int(mySocket.recv(6))
        for i in range(length):   
            data += mySocket.recv(1024)

        #save picture
        with open ('Picture.png','wb') as file:
            file.write(data)

        print("recived")
        send_message("","ok",mySocket)
        print("sent confirmation")          

#loads a picture and locate crates and places to put them in
def process_picture(list):
    # load yolov8 model
    model = YOLO('best.pt')

    # load picture
    picture_path = 'lol.png'
    frame = cv2.imread(picture_path)

    #uses the yolov8 model to find crates and places to put them in
    results = model.track(frame, persist=True, conf = 0.1, iou = 0.1)
    frame_ = results[0].plot()
        
    #save picture
    cv2.imwrite("AfterCode.png", frame_)

#request the server to take a picture and to send the picture, then it saves the picture, process it and update the picture on screen
def refresh(UDPClient,screen,boxPlaces):
    send_message("take_picture()","do",UDPClient)
    send_message('send_message("Picture.png","picture",mySocket)',"do",UDPClient)
    receive_message(UDPClient)
    process_picture(boxPlaces)  
    screen.blit(pygame.image.load('AfterCode.png'), (0, 0))
    pygame.display.flip()

#gets user input on what crate to pick up and where to put it
def select(screen, boxes):
    print("select")
    while pygame.mouse.get_pressed()[2] == True:
        pass
    print("1")
    while pygame.mouse.get_pressed()[2] == False:
        pass
    print("2")
    for box in boxes:
        if box.x < pygame.mouse.get_pos()[0] and box.x+box.w > pygame.mouse.get_pos()[0] and box.y < pygame.mouse.get_pos()[1] and box.y+box.h > pygame.mouse.get_pos()[1]:
            print(box.middlePoint)
            return box

#open a pygame window which the user can select the crate and where to put it
def set_up():
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1030
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Project")

    screen.blit(pygame.image.load('AfterCode.png'), (0, 0))

    return screen

