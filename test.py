# import pygame package
import pygame
import protocol
import classes
import socket
import time
 
screen = protocol.setUp()
 
refresh = classes.button(800,200,300,100,screen, "protocol.refresh(UDPClient,screen,boxPlaces)","refresh")
select = classes.button(1200,200,300,100,screen, "protocol.select(screen, boxPlaces)","select")
buttons = [refresh,select]
boxPlaces = []
refresh.drawButton()
select.drawButton()
pygame.display.flip()

serverAddress = ('127.0.0.1',8888)

UDPClient=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
UDPClient.connect(serverAddress)
protocol.refresh(UDPClient,screen,buttons)

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
                    time.sleep(1)

        
        