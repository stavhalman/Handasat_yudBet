import socket
import cv2

def takePicture():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port) 
    
    result, image = cam.read() 
    
    if result: 

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
    x = mySocket.recv(1).decode()
    print(x)    
    messageTypeLength:int = int(x)

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

