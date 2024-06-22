import socket
import Protocol
import RPi.GPIO as GPIO

def main():
    # this file runs on the sudpberry pi, the file purpose is to recive orders and execute them
    ServerPort=8888
    ServerIP='0.0.0.0'

    RPISocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    RPISocket.bind((ServerIP,ServerPort))

    print("server is up")
    RPISocket.listen()
    clientSocket,clientAddress = RPISocket.accept()

    while True:
        Protocol.receive_message(clientSocket)
        print("done")

step2 = 17
step1 = 16
dir2 = 23
dir1 = 24
enb = 21

speed = 1
current_x = 0
current_y = 0
max_x = 1300
max_y = 1400

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(step1, GPIO.OUT)
    GPIO.setup(step2, GPIO.OUT)
    GPIO.setup(dir1, GPIO.OUT)
    GPIO.setup(dir2, GPIO.OUT)
    GPIO.setup(enb, GPIO.OUT)


    GPIO.output(enb, GPIO.HIGH)
    main()
    Protocol.shut_down()
