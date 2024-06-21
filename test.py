# import pygame package
import pygame
import Protocol
import Classes
import socket
import time
 
screen = Protocol.set_up()
 
refresh = Classes.button(800,200,300,100,screen, "Protocol.refresh(UDPClient,screen,boxPlaces)","refresh")
select = Classes.button(1200,200,300,100,screen, "Protocol.select(screen, boxPlaces)","select")
buttons = [refresh,select]
boxPlaces = []
refresh.drawButton()
select.drawButton()
pygame.display.flip()

serverAddress = ('127.0.0.1',8888)

UDPClient=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
UDPClient.connect(serverAddress)
Protocol.refresh(UDPClient,screen,buttons)

running = True
while running:

    # Check for event if user has pushed 
    # any event in queue
    for event in pygame.event.get():
       
        # if event is of type quit then set
        # running bool to false
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.x < pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < button.x+button.w and button.y < pygame.mouse.get_pos()[1] and pygame.mouse.get_pos()[1] < button.y+button.h:
                    eval(button.action)

        
        