import pygame
import random
import a_config
from a_config import *
from pygame.locals import *

ancho = 48

class Escudo(pygame.sprite.Sprite):
    def __init__(self):
        super(Escudo, self).__init__()
        
        self.surf = pygame.image.load("src/sprites/pickups/escudochico.png")
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(ANCHO, random.randrange(int(ALTURA * .5), int(ALTURA * .8)))
        self.velocidad = random.randrange(2, 4) / 10
        
    def update(self, tiempo_lol):
        self.pos.x -= self.velocidad * a_config.velocidad_juego * tiempo_lol
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

        if (self.rect.x + ancho) < 0:
            self.kill()