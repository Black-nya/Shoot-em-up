import pygame
from random import *

class Small(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0],bg_size[1]
        self.speed = 2
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),randint(-5*self.height,0)
        self.destroy_images = [\
            pygame.image.load("images/enemy1_down1.png").convert_alpha(),\
            pygame.image.load("images/enemy1_down2.png").convert_alpha(),\
            pygame.image.load("images/enemy1_down3.png").convert_alpha(),\
            pygame.image.load("images/enemy1_down4.png").convert_alpha()
                               ]
        self.live = True
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.live = True
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),randint(-5*self.height,0)
        
        
class Medium(pygame.sprite.Sprite):
    health = 8
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy2.png").convert_alpha()
        self.image_hit = pygame.image.load("images/enemy2_hit.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0],bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),randint(-10*self.height,-self.height)
        self.destroy_images = [\
            pygame.image.load("images/enemy2_down1.png").convert_alpha(),\
            pygame.image.load("images/enemy2_down2.png").convert_alpha(),\
            pygame.image.load("images/enemy2_down3.png").convert_alpha(),\
            pygame.image.load("images/enemy2_down4.png").convert_alpha()
                               ]
        self.live = True
        self.mask = pygame.mask.from_surface(self.image)
        self.health = Medium.health
        self.hit = False
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.health = Medium.health
        self.live = True
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),randint(-5*self.height,0)
        
        
class Large(pygame.sprite.Sprite):
    health = 20
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("images/enemy3_n1.png").convert_alpha()
        self.image2 = pygame.image.load("images/enemy3_n2.png").convert_alpha()
        self.image_hit = pygame.image.load("images/enemy3_hit.png").convert_alpha()
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0],bg_size[1]
        self.speed = 0.5
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),randint(-15*self.height,-5*self.height)
        self.destroy_images = [\
            pygame.image.load("images/enemy3_down1.png").convert_alpha(),\
            pygame.image.load("images/enemy3_down2.png").convert_alpha(),\
            pygame.image.load("images/enemy3_down3.png").convert_alpha(),\
            pygame.image.load("images/enemy3_down4.png").convert_alpha(),\
            pygame.image.load("images/enemy3_down5.png").convert_alpha(),\
            pygame.image.load("images/enemy3_down6.png").convert_alpha()
                               ]
        self.live = True
        self.mask = pygame.mask.from_surface(self.image1)
        self.health = Large.health
        self.hit = False
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.live = True
        self.health = Large.health
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),randint(-5*self.height,0)
        
        
