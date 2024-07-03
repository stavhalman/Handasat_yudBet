import pygame
import Classes
import random

pygame.init()

display_size = (1920,1030)

screen = pygame.display.set_mode(display_size)
screen.blit(pygame.image.load("background.png"),(0,0))
keys = {"up":pygame.K_w,"down":pygame.K_s,"right":pygame.K_d,"left":pygame.K_a}
player1 = Classes.Player(1000,500,"stickman.png",100,0,[],[],keys)
objects = []
for i in range(100000):
    objects.append(Classes.Game_Object(random.randrange(-50000,50000),random.randrange(-50000,50000),"tree.png",100,0,{Classes.Item("wood",random.randint(3,5))}))

pygame.display.flip()

clock = pygame.time.Clock()
fps = 60

running = True
while running:


    # Check for event if user has pushed 
    # any event in queue
    for event in pygame.event.get():
        
        # if event is of type quit then set
        # running bool to false
        if event.type == pygame.QUIT:
            running = False
 
    
    screen.blit(pygame.image.load("background.png"),(0,0))
    player1.update(screen,objects)
    pygame.display.flip()
    clock.tick(fps)