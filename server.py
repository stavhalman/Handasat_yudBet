import socket
import Protocol_Server
import RPi.GPIO as GPIO


def main():

    # this file runs on the sudpberry pi, the file's purpose is to recive orders and execute them
    while True:
        Protocol_Server.receive_message()
        print("done")



if __name__ == "__main__":

    #set pins
    step2 = 17
    step1 = 16
    dir2 = 23
    dir1 = 24
    enb = 21

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(step1, GPIO.OUT)
    GPIO.setup(step2, GPIO.OUT)
    GPIO.setup(dir1, GPIO.OUT)
    GPIO.setup(dir2, GPIO.OUT)
    GPIO.setup(enb, GPIO.OUT)
    
    #set speed and boarders
    speed = 1
    current_x = 0
    current_y = 0
    max_x = 1300
    max_y = 1400
    state = 0
    
    #waits for a cleint to connect
    ServerPort=8888
    ServerIP='0.0.0.0'

    RPISocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    RPISocket.bind((ServerIP,ServerPort))

    print("server is up")
    RPISocket.listen()
    clientSocket,clientAddress = RPISocket.accept()

    Protocol_Server.send_message(str(current_x)+","+str(current_y)+","+str(max_x)+","+str(max_y)+","+str(state),"info")

    main()