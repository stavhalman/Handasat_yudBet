# import pygame package
import pygame
import Protocol_Client
import Classes
import socket
import time
 

def main():
    global screen,boxPlaces,buttons
    Protocol_Client.refresh(UDPClient,screen)

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

if __name__ == "__main__":

    serverAddress = ('127.0.0.1',8888)

    UDPClient=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    UDPClient.connect(serverAddress)

    current_x,current_y,max_x,max_y = tuple(map(int, Protocol_Client.receive_message().split(',')))

    screen,buttons,boxPlaces = Protocol_Client.set_up(),[]

    for button in buttons:
        button.draw_button()

    pygame.display.flip()

    main()