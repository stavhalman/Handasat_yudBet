import socket
import Protocol_Server
import RPi.GPIO as GPIO

def main():

    # this file runs on the sudpberry pi, the file's purpose is to recive orders and execute them
    while True:
        while is_client:
            Protocol_Server.receive_message()
            print("done")
        Protocol_Server.get_client()

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
    
    is_client = False

    #waits for a cleint to connect
    ServerPort=8888
    ServerIP='0.0.0.0'

    clientSocket = Protocol_Server.get_client()

    main()