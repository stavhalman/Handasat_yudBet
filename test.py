
# import pygame package
import pygame
 
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1030
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Project")

screen.blit(pygame.image.load('AfterCode.png'), (0, 0))
pygame.display.flip()
 
# creating a bool value which checks 
# if game is running
running = True
 
# Game loop
# keep game running till running is true
while running:
   
    # Check for event if user has pushed 
    # any event in queue
    for event in pygame.event.get():
       
        # if event is of type quit then set
        # running bool to false
        if event.type == pygame.QUIT:
            running = False