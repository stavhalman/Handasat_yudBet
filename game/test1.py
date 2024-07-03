import pygame


pygame.init()

screen = pygame.display.set_mode((1920,1030))
screen.blit(pygame.image.load("background.png"),(0,0))
pygame.draw.rect(screen,(255,0,0),(1920/2-100,1030/2-200,200,400))
pygame.display.flip()

running = True
while running:


    # Check for event if user has pushed 
    # any event in queue
    for event in pygame.event.get():
        
        # if event is of type quit then set
        # running bool to false
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            screen.blit(pygame.image.load("background.png"),(0,0))
            pygame.draw.rect(screen,(255,0,0),(400,1030/2-200,200,400))
            pygame.display.flip()