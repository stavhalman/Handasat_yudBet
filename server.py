import socket
import Protocol_Server
import RPi.GPIO as GPIO
import time

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
    button1 = 19
    button2 = 13
    servo_pin = 13
    encoder = 13

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(step1, GPIO.OUT)
    GPIO.setup(step2, GPIO.OUT)
    GPIO.setup(dir1, GPIO.OUT)
    GPIO.setup(dir2, GPIO.OUT)
    GPIO.setup(enb, GPIO.OUT)
    GPIO.setup(button1, GPIO.IN)
    GPIO.setup(button2, GPIO.IN)
    GPIO.setup(servo_pin, GPIO.OUT)
    GPIO.setup(encoder, GPIO.IN)

    servo = GPIO.PWM(servo_pin,30)

    servo.start(0)
    servo.ChangeDutyCycle(2)
    time.sleep(1)
    
    
    #set speed and boarders
    speed = 1
    current_x = 0
    current_y = 0
    max_x = 1300
    max_y = 1400
    current_z = 0
    
    is_client = False

    #waits for a cleint to connect
    ServerPort=8888
    ServerIP='0.0.0.0'

    clientSocket = Protocol_Server.get_client()

    main()