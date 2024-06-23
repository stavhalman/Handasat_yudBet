import socket
import cv2
from ultralytics import YOLO
import pygame
from Client import *
import mouse


#open a pygame window which the user can select the crate and where to put it
def set_up():
    global max_x,max_y
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1030
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Project")

    screen.blit(pygame.image.load('AfterCode.png'), (0, 0))

    refresh = Classes.button(800,200,300,100,screen, "Protocol_Client.refresh()","refresh")
    select = Classes.button(1200,200,300,100,screen, "Protocol_Client.select()","select")
    move_to_middle = Classes.button(1200,600,300,100,screen, "Protocol_Client.move_to_cords("+str(max_x/2)+","+str(max_y/2)+")","move to middle")
    buttons = [refresh,select,move_to_middle]

    return screen,buttons

#a function to run before shutting down
def shut_down():
    send_message("shut_down()","do")

#makes the server to take a picture and saves it and sent it back
def take_picture():
    send_message("take_picture()","do")
    send_message('send_message("Picture.png","picture",mySocket)',"do")
    receive_message()

#recieves cordinations and makes the server to move to them
def move_to_cords(target_x,target_y):
    send_message("move_to_cords("+target_x+","+target_y+")","do")

#recive a message (string), message type (string) and socket. sends message to socket
def send_message(message:str,messageType):
    global UDPClient

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
        UDPClient.send(start)
    else:

        #constract message by order
        message = messageTypeLength+messageType+message

        #encode message
        message = message.encode()
    
    #send message
    UDPClient.send(message)
    if( messageType != "ok"):
        print("sent")
        receive_message(UDPClient)
        print("confirmed")

#recive a socket and recive a message from it, acts acording to message type
def receive_message():
    global UDPClient

    #get socket type length
    messageTypeLength:int = int(UDPClient.recv(1).decode())
    print(messageTypeLength)

    #get the socket type
    messageType = UDPClient.recv(messageTypeLength).decode()   
    print(messageType) 
    

    if messageType == "do":

        #get command
        message = UDPClient.recv(1024).decode()

        print("recived")
        send_message("","ok",UDPClient)
        print("sent confirmation")

        #do command
        print("doing: "+message)
        eval(message)

    
    elif messageType == "picture":

        #def a bytes veriable
        data:bytes = b''

        #recive all the bytes of the picture
        length = int(UDPClient.recv(6))
        for i in range(length):   
            data += UDPClient.recv(1024)

        #save picture
        with open ('Picture.png','wb') as file:
            file.write(data)

        print("recived")
        send_message("","ok",UDPClient)
        print("sent confirmation")          

#loads a picture and locate crates and places to put them in
def process_picture():
    global boxPlaces
    # load yolov8 model
    model = YOLO('best.pt')

    # load picture
    picture_path = 'Picture.png'
    frame = cv2.imread(picture_path)

    #uses the yolov8 model to find crates and places to put them in
    results = model.track(frame, persist=True, conf = 0.4, iou = 0.4)
    frame_ = results[0].plot()
        
    #save picture
    cv2.imwrite("AfterCode.png", frame_)
    boxPlaces=[]
    middle_x = 0
    middle_y = 0
    if(len(results[0].boxes) != 0):
        for bx in results[0].boxes:
            boxPlaces.append(bx)
            temp_middle_x = (bx.xyxy[0][0] + bx.xyxy[0][2])/2
            temp_middle_y = (bx.xyxy[0][1] + bx.xyxy[0][3])/2
            if pow(middle_x-320)+pow(middle_y-240)>pow(temp_middle_x-320)+pow(temp_middle_y-240):
                middle_x = temp_middle_x
                middle_y = temp_middle_y
        return middle_x,middle_y
    else:
        print("empty")
        return -1000,-1000

#request the server to take a picture and to send the picture, then it saves the picture, process it and update the picture on screen
def refresh():
    global screen
    take_picture()
    x,y = process_picture()  
    screen.blit(pygame.image.load('AfterCode.png'), (0, 0))
    pygame.display.flip()
    return x,y

#gets user input on what crate to pick up and where to put it
def select():
    global boxPlaces

    while mouse.is_pressed("left") == True:
        pass
    while mouse.is_pressed("left") == False:
        pass

    for box in boxPlaces:
        if int(box.xyxy[0][0]) < mouse.get_position()[0]  and int(box.xyxy[0][2]) > mouse.get_position()[0] and int(box.xyxy[0][1]) < mouse.get_position()[1]  and int(box.xyxy[0][3]) > mouse.get_position()[1]:
            pick_up(int(box.xyxy[0][0])+int(box.xyxy[0][2])-320,240-int(box.xyxy[0][1])+int(box.xyxy[0][3]))
            return True
    return False

#a function that recives cordinates and trie to pick up a crate there
def pick_up(x,y):
    global current_x,current_y

    move_to_cords(current_x+x,current_y+y)

    temp_x,temp_y = refresh()
    if(temp_x == -1000 and temp_y == -1000):
        print("no pick up found")
        return False
    if(temp_x!=x or temp_y!=y):
        move_to_cords(temp_x,temp_y)
    
    send_message("pick_up()","do")
    return True

#a function that recives cordinates and trie to put down a crate there
def put_down(x,y):
    global current_x,current_y

    move_to_cords(current_x+x,current_y+y)

    temp_x,temp_y = refresh()
    if(temp_x == -1000 and temp_y == -1000):
        print("no put down found")
        return False
    if(temp_x!=x or temp_y!=y):
        move_to_cords(temp_x,temp_y)
    
    send_message("put_down()","do")
    return True