import pygame
from a_config import *
import random
import a_config

altura_plataforma = 64
ancho_bloque = 64
altura_bloque = 64

class PlataformaJuego(pygame.sprite.Sprite):
    bloques = [
        {
            "1": "1-3.png",
            "2": "2.png",
            "3": "1-3.png",
            "4": "3.png"
        },
        {
            "1": "b_1-3.png",
            "2": "b_2.png",
            "3": "b_1-3.png",
            "4": "b_4.png"
        },
        {
            "1": "c_1-3.png",
            "2": "c_2.png",
            "3": "c_1-3.png",
            "4": "c_4.png"
        }
    ]

    def __init__(self, numero_bloques, x):
        super(PlataformaJuego, self).__init__()

        ancho = numero_bloques * ancho_bloque
        self.altura = random.randint(16, 256)
        self.surf = pygame.Surface((ancho, self.altura), pygame.SRCALPHA)

        indice_bloque = random.randrange(len(self.bloques))
        bloque = self.bloques[indice_bloque]

        surf_bloque_1 = pygame.image.load("src/sprites/bloques/" + bloque['1']).convert_alpha()
        surf_bloque_2 = pygame.image.load("src/sprites/bloques/" + bloque['2']).convert_alpha()
        surf_bloque_3 = pygame.image.load("src/sprites/bloques/" + bloque['3']).convert_alpha()
        surf_bloque_4 = pygame.image.load("src/sprites/bloques/" + bloque['4']).convert_alpha()

        surf_bloque_1 = pygame.transform.scale(surf_bloque_1, (ancho_bloque, altura_bloque))
        surf_bloque_2 = pygame.transform.scale(surf_bloque_2, (ancho_bloque, altura_bloque))
        surf_bloque_3 = pygame.transform.scale(surf_bloque_3, (ancho_bloque, altura_bloque))
        surf_bloque_4 = pygame.transform.scale(surf_bloque_4, (ancho_bloque, altura_bloque))

        if numero_bloques == 1:
            self.surf.blit(surf_bloque_1, (0, 0))
        else:
            for indice in range(numero_bloques):
                x_bloque = indice * ancho_bloque
                if indice == 0:
                    self.surf.blit(surf_bloque_2, (x_bloque, 0))
                elif x_bloque + ancho_bloque >= ancho:
                    self.surf.blit(surf_bloque_4, (x_bloque, 0))
                else:
                    self.surf.blit(surf_bloque_3, (x_bloque, 0))

        self.posicion = pygame.math.Vector2(x, ALTURA - self.altura)
        self.rect = self.surf.get_rect(topleft=(x, self.posicion.y))
        self.velocidad = 0.3
        self.surf = self.surf.convert_alpha()

    def actualizar(self, delta_tiempo):
        self.posicion.x -= self.velocidad * a_config.velocidad_juego * delta_tiempo
        self.rect.topleft = self.posicion
