
# import pygame package
import pygame
import protocol
import classes
import socket
 
screen = protocol.setUp()
 
refresh = classes.button(800,200,300,100,screen, "protocol.refresh(UDPClient,screen)","refresh")
select = classes.button(1200,200,300,100,screen, "protocol.select(results)","select")
buttons = {refresh,select}
refresh.drawButton()
select.drawButton()
pygame.display.flip()

serverAddress = ('10.0.0.22',8888)

UDPClient=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
UDPClient.connect(serverAddress)

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
        
        