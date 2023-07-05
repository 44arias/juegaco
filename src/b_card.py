import pygame
from pygame.locals import *
from a_config import *
import a_config
import random

ancho = 48
altura = 48
tamaño_asset = 24

class Card(pygame.sprite.Sprite):
    def __init__(self):
        super(Card, self).__init__()

        self.animacion_actual = 'idle'
        self.animations = {}
        self.animacion_anterior = {
            'idle': 'continuous'
        }

        self.cargar_recursos()

        self.indice_animacion = 0
        self.velocidad_animacion = .15

        self.surf = self.animations[self.animacion_actual][self.indice_animacion]
        self.surf = pygame.transform.scale(self.surf, (ancho, altura))
        self.rect = self.surf.get_rect()

        self.pos = pygame.math.Vector2(ANCHO, random.randrange(int(ALTURA*.5), int(ALTURA*.8)))

        self.velocidad = random.randrange (2,4) / 10

    def cargar_recursos(self):
        self.animations['idle'] = []

        asset = pygame.image.load("src/sprites/pickups/card.png").convert_alpha()
        self.ancho = asset.get_width()
        indice = 0

        while (indice * tamaño_asset < self.ancho):
            frame = pygame.Surface((tamaño_asset, tamaño_asset), pygame.SRCALPHA)
            frame.blit(asset, asset.get_rect(), Rect(indice * tamaño_asset, 0, tamaño_asset, tamaño_asset))
            self.animations['idle'].append(frame.convert_alpha())
            indice += 1

    def animar(self,tiempo_lol):
        self.velocidad_animacion = .008 * tiempo_lol

        self.indice_animacion += self.velocidad_animacion

        if int(self.indice_animacion)+1 >= len(self.animations[self.animacion_actual]):
            if self.animacion_anterior[self.animacion_actual] == 'continuous':
                self.indice_animacion = 0
            else:
                self.indice_animacion = len(self.animations[self.animacion_actual])-1

        self.surf = self.animations[self.animacion_actual][int(self.indice_animacion)]
        self.surf = pygame.transform.scale(self.surf, (ancho, altura))
        self.rect = self.surf.get_rect()

    def update(self, tiempo_lol):
        self.animar(tiempo_lol)

        self.pos.x -= self.velocidad * a_config.velocidad_juego * tiempo_lol
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

        if (self.rect.x + ancho) < 0:
            self.kill()