import pygame

ANCHO = 1280 
ALTURA = 720 
ANCHO_2 = 90
ALTURA_2 = 90

ANCHO_HITBOX = 60
ALTURA_HITBOX = 100

VELOCIDAD_CORRER = 5

TAMAÑO_ASSET = 48

FUERZA_SALTO = 11

FPS = 60

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)

generar_nueva_plataforma = pygame.USEREVENT + 1
generar_dinero = pygame.USEREVENT + 2
generar_escudo = pygame.USEREVENT + 3
generar_card = pygame.USEREVENT + 4
generar_enemigo = pygame.USEREVENT + 5

generar_mensaje_dificultad = pygame.USEREVENT + 6

velocidad_juego = 1
gravedad = 9.8

