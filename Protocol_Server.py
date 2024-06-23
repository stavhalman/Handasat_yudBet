import socket
import cv2
from ultralytics import YOLO
import time
import RPi.GPIO as GPIO
from multiprocessing import Process
from Server import *

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

#moves a motor for a selected time and speed
def move_motor(step_Pin,dir_Pin,dir,move_Time,speed):
    GPIO.output(dir_Pin, dir)
    loops = int(move_Time*1000*speed)
    delay = 0.0005/speed
    for i in range(loops):
        GPIO.output(step_Pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(step_Pin, GPIO.LOW)
        time.sleep(delay)

#recieves cordinations and moves to them
def move_to_cords(target_x,target_y):
    global max_x,max_y, current_x, current_y, speed
    if(target_x<0 or target_x>max_x) or target_y<0 or target_y>max_y:
        print("requested cords are out of bounds")
        return False
    x_move = target_x-current_x
    y_move = target_y-current_y
    time_to_move = (abs(x_move/1000)+abs(y_move/1000))/speed

    if(x_move>abs(y_move) or abs(x_move)<y_move or (x_move==y_move and x_move>0)):
        dir_motor1 = GPIO.HIGH
    else:
        dir_motor1 = GPIO.LOW

    if(x_move>abs(y_move) or abs(x_move)<-y_move or (x_move==-y_move and x_move>0)):
        dir_motor2 = GPIO.HIGH
    else:
        dir_motor2 = GPIO.LOW

    
        
    if(x_move==0):
        t1 = Process(target = move_motor, args = (step1,dir1,dir_motor1,time_to_move,speed))
        t2 = Process(target = move_motor, args = (step2,dir2,dir_motor2,time_to_move,speed))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    elif (x_move == y_move):
        move_motor(step1,dir1,dir_motor1,time_to_move,speed)
    elif (x_move == -y_move):
        move_motor(step2,dir2,dir_motor2,time_to_move,speed)
    else:
        speed1 = abs(x_move/2+y_move/2)
        speed2 = abs(x_move/2-y_move/2)
        if(speed1>speed2):
            speed2=speed2/speed1
            speed1 = 1
        else:
            speed1=speed1/speed2
            speed2 = 1
        print(speed1)
        print(speed2)
        t1 = Process(target = move_motor, args = (step1,dir1,dir_motor1,time_to_move,speed1))
        t2 = Process(target = move_motor, args = (step2,dir2,dir_motor2,time_to_move,speed2)) 
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        

    current_x = target_x
    current_y = target_y

#a function to run before shutting down
def shut_down():
    move_to_cords(0,0)
    GPIO.output(enb, GPIO.LOW)
    GPIO.cleanup()

#recive a message (string), message type (string) and socket. sends message to socket
def send_message(message:str,messageType):
    global clientSocket

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
        clientSocket.send(start)
    else:

        #constract message by order
        message = messageTypeLength+messageType+message

        #encode message
        message = message.encode()
    
    #send message
    clientSocket.send(message)
    if( messageType != "ok"):
        print("sent")
        receive_message(clientSocket)
        print("confirmed")

#recive a socket and recive a message from it, acts acording to message type
def receive_message():
    global clientSocket

    #get socket type length
    messageTypeLength:int = int(clientSocket.recv(1).decode())
    print(messageTypeLength)

    #get the socket type
    messageType = clientSocket.recv(messageTypeLength).decode()   
    print(messageType) 
    

    if messageType == "do":

        #get command
        message = clientSocket.recv(1024).decode()

        print("recived")
        send_message("","ok",clientSocket)
        print("sent confirmation")

        #do command
        print("doing: "+message)
        eval(message)

    
    elif messageType == "picture":

        #def a bytes veriable
        data:bytes = b''

        #recive all the bytes of the picture
        length = int(clientSocket.recv(6))
        for i in range(length):   
            data += clientSocket.recv(1024)

        #save picture
        with open ('Picture.png','wb') as file:
            file.write(data)

        print("recived")
        send_message("","ok",clientSocket)
        print("sent confirmation")         

    elif messageType == "info":

        info = clientSocket.recv(1024)

        print("recived")
        send_message("","ok",clientSocket)
        print("sent confirmation")

        return info

#a function that pick up a crate below
def pick_up():
    print("picking up")

#a function that puts down a crate below
def put_down():
    print("putting down")

