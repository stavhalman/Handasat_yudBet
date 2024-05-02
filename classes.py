import pygame

class button:
    def __init__(self, x, y, w, h, screen, action, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.screen = screen
        self.action = action
        self.text = text
    
    def drawButton(self):
        font = pygame.font.SysFont('freesanbold.ttf', 50)
        text = font.render(self.text, True, (255, 255, 255))
        textRect1 = text.get_rect()
        textRect1.center = (self.x+self.w/2, self.y+self.h/2)
        pygame.draw.rect(self.screen,(255,255,255),[self.x,self.y,self.w,self.h],5)
        self.screen.blit(text, textRect1)
    
