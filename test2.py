# import pygame package
import pygame
import Protocol
import Classes
import socket
import time


serverAddress = ('192.168.0.102',8888)

UDPClient=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
UDPClient.connect(serverAddress)

Protocol.send_message("GPIO.output(enb,GPIO.HIGH)","do",UDPClient)
Protocol.send_message("move_to_cords(300,300)","do",UDPClient)
Protocol.send_message("GPIO.output(enb,GPIO.LOW)","do",UDPClient)
time.sleep(10)