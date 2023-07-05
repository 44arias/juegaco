import pygame
from pygame.locals import *
import random
import json
from a_config import *
import a_config 
from b_plataformas import PlataformaJuego
from jugador import Jugador
from b_dinero import Dinero
from b_card import Card
from b_enemigo import Enemigo
from b_escudo import Escudo
import os

def get_font(size): 
    return pygame.font.Font("src/fonts/font.ttf", size)

class Juego:
    def __init__(self):
        pygame.init()
        
        pygame.display.set_caption("Salto saltito")

        self.pantalla = pygame.display.set_mode([ANCHO, ALTURA])
        self.reloj = pygame.time.Clock()
        self.ejecutando = True
        
        pygame.mouse.get_cursor()

        self.fondo_1 = pygame.transform.scale(pygame.image.load("src/sprites/otros sprites/menu.jpg"), (ANCHO, ALTURA))
        self.fondo_3 = pygame.transform.scale(pygame.image.load("src/sprites/otros sprites/game-over.jpg"), (ANCHO, ALTURA))

        self.fuente = get_font(70)
        self.fuente_mas_pequeña = get_font(40)
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        
        pygame.mixer.music.load("src/sounds/fondo.mp3")
        pygame.mixer.music.set_volume(.05)
        self.sonido_muerte = pygame.mixer.Sound("src/sounds/death.mp3")
        self.sonido_muerte.set_volume(.01)
        self.sonido_gamerover = pygame.mixer.Sound("src/sounds/gameover.mp3")
        self.sonido_gamerover.set_volume(.05)
        self.sonido_salvada = pygame.mixer.Sound("src/sounds/salvada.mp3")
        self.sonido_salvada.set_volume(.05)
        
        self.inicializar()

    def inicializar(self):
        self.jugador = Jugador()
        self.no_face = False
        self.muerto = False
        
        self.plataformas = []
        plataforma = PlataformaJuego(20, 0)
        self.plataformas.append(plataforma)
        self.grupo_plataformas = pygame.sprite.Group()
        self.grupo_plataformas.add(plataforma)
        self.plataforma_se_creara = False
        
        self.dificultad = 1
        self.tiempo_inicio = pygame.time.get_ticks()
        self.ultimo_tiempo_frame = -1
        self.puntuacion = 0
        self.puntuacion_lol = 0
        self.texto_puntuacion = None
        self.rect_texto_puntuacion = None
        self.dificultad_anterior = 1
        self.rect_lol = None
        self.i = 0
        self.flag_segundo_mensaje = True
        self.subiendo_dificultad = None
        self.rect_mostrar_texto_dificultad = None
        
        self.dinero = []
        self.grupo_dinero = pygame.sprite.Group()
        pygame.time.set_timer(generar_dinero, 1000)
        
        self.card = []
        self.grupo_cards = pygame.sprite.Group()
        pygame.time.set_timer(generar_card, 20000)
        
        self.escudo = []
        self.grupo_escudos = pygame.sprite.Group()
        pygame.time.set_timer(generar_escudo, 10000)
                
        self.enemigos = []
        self.grupo_enemigos = pygame.sprite.Group()
        pygame.time.set_timer(generar_enemigo, 5000)
        
        self.high_score = self.obtener_high_score()
                
        pygame.mixer.music.play(-1)

    def actualizar(self, tiempo_lol):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    self.jugador.saltar()
                elif evento.key == pygame.K_s:
                    self.jugador.cancelar_salto()
                elif self.muerto and evento.key == pygame.K_RETURN:
                    self.inicializar()
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.stop(self.sonido_gamerover)
                    
            elif evento.type == generar_nueva_plataforma:
                self.plataforma_se_creara = False
                
                minimo = 1 
                if self.dificultad <= 3 :
                    minimo = 1
                else:
                    minimo = 3
                
                maximo = 12 - self.dificultad 
                if 12 - self.dificultad > 3:
                    maximo = 12
                else:
                    maximo = 4
                    
                numero_bloques = random.randrange(minimo, maximo)
                
                espacio_minimo = 90 + self.dificultad * 2
                if 90 + self.dificultad * 2 <= 150:
                    espacio_minimo = 90
                else:
                    espacio_minimo = 150
                
                espacio_maximo = 200 + self.dificultad * 2 
                if 200 + self.dificultad * 2 <= 350:
                    espacio_maximo = 200
                else:
                    espacio_maximo = 350
                    
                espacio = random.randrange(espacio_minimo, espacio_maximo)
                plataforma = PlataformaJuego(numero_bloques, ANCHO + espacio)
                self.plataformas.append(plataforma)
                self.grupo_plataformas.add(plataforma)
                
            elif evento.type == generar_dinero:
                dinero = Dinero()
                self.dinero.append(dinero)
                self.grupo_dinero.add(dinero)
                
                tiempo_minimo = 4000 - self.dificultad * 500 
                if tiempo_minimo < 2000:
                    tiempo_minimo = 2000
                    
                tiempo_maximo = 10000 - self.dificultad * 500 
                if tiempo_maximo < 4000:
                    tiempo_maximo = 4000

                pygame.time.set_timer(generar_dinero, 1000)
                
            elif evento.type == generar_card:
                if self.dificultad > 5:
                    break
                else:
                    card = Card()
                    self.card.append(card)
                    self.grupo_cards.add(card)
                    tiempo_minimo = 4000 - self.dificultad * 500 
                    if tiempo_minimo < 2000:
                        tiempo_minimo = 2000
                
                    tiempo_maximo = 10000 - self.dificultad * 500 
                    if tiempo_maximo < 4000:
                        tiempo_maximo = 4000
                        
                    pygame.time.set_timer(generar_card, random.randint(10000, 20000))
                
            elif evento.type == generar_escudo:
                if self.dificultad > 8:
                    break
                elif not self.jugador.tiene_escudo:
                    escudo = Escudo()
                    self.escudo.append(escudo)
                    self.grupo_escudos.add(escudo)
                    tiempo_minimo = 4000 - self.dificultad * 500 
                    if tiempo_minimo < 2000:
                        tiempo_minimo = 2000
                        
                    tiempo_maximo = 10000 - self.dificultad * 500 
                    if tiempo_maximo < 4000:
                        tiempo_maximo = 4000
                        
                    pygame.time.set_timer(generar_escudo, random.randint(15000, 20000))
                
            elif evento.type == generar_enemigo:
                enemigo = Enemigo()
                self.enemigos.append(enemigo)
                self.grupo_enemigos.add(enemigo)
                tiempo_minimo = 4000 - self.dificultad * 500 
                if tiempo_minimo < 2000:
                    tiempo_minimo = 2000
                    
                tiempo_maximo = 10000 - self.dificultad * 500 
                if tiempo_maximo < 4000:
                    tiempo_maximo = 4000
                    
                pygame.time.set_timer(generar_enemigo, random.randint(tiempo_minimo, tiempo_maximo))
                
        if not self.jugador.muerto:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()
                
        if self.muerto or self.no_face:
            return
        
        self.jugador.actualizar(tiempo_lol, self.grupo_plataformas, self.grupo_dinero, self.grupo_cards, self.grupo_escudos, self.grupo_enemigos)
        
        if self.jugador.muerto or self.jugador.rect.top > ALTURA:
            if self.jugador.tiene_escudo:
                self.jugador.guardar_con_escudo()
                pygame.mixer.Sound.play(self.sonido_salvada)
            else:
                self.muerto = True
                pygame.mixer.Sound.play(self.sonido_muerte)
                
            
        if self.jugador.sumar_puntuacion > 0:
            self.puntuacion += self.jugador.sumar_puntuacion * 1000
            self.jugador.sumar_puntuacion = 0
            
        for plataforma in self.plataformas:
            plataforma.actualizar(tiempo_lol)
            
        self.grupo_dinero.update(tiempo_lol)
        self.grupo_cards.update(tiempo_lol)
        self.grupo_escudos.update(tiempo_lol) 
        self.grupo_enemigos.update(tiempo_lol)
        
        if ANCHO - self.plataformas[-1].rect.right > 0:
            self.plataforma_se_creara = True
            pygame.event.post(pygame.event.Event(generar_nueva_plataforma))

        segundos = int((pygame.time.get_ticks() - self.tiempo_inicio) / 1000)
        self.dificultad = 1 + segundos // 10
        a_config.velocidad_juego = 1 + self.dificultad * 0.2

        self.puntuacion += a_config.velocidad_juego * tiempo_lol
        
        self.puntuacion_lol = int(self.puntuacion/1000)
    
        self.texto_puntuacion = get_font(40).render('Score: ' + str(self.puntuacion_lol), True, (255, 255, 255))
        self.rect_texto_puntuacion = self.texto_puntuacion.get_rect()
        self.rect_texto_puntuacion.y = 12
        self.rect_texto_puntuacion.x = (ANCHO//2) - (self.rect_texto_puntuacion.width//2)
        
        self.subiendo_dificultad = get_font(30).render('Mmm... subiendo la dificultad...', True, (255, 255, 255))
        self.mas_dificultad = get_font(30).render('Subiendo AÚN MÁS la dificultad...', True, (255, 255, 255))
        self.y = get_font(30).render('Y...', True, (255, 255, 255))
        self.chau_escudo = get_font(30).render('Sin ESCUDOS...?', True, (0, 0, 0))      
        
        
    def textos_dificultades(self, texto, tamaño, color):
        self.subiendo_dificultad = get_font(tamaño).render(texto, True, color)
        return self.subiendo_dificultad
            
    def renderizar(self):
        self.pantalla.fill('#b2afba')
        # self.pantalla.blit(self.fondo_1, (0, 0))

        for plataforma in self.plataformas:
            self.pantalla.blit(plataforma.surf, plataforma.rect)

        self.pantalla.blit(self.jugador.surf, self.jugador.rect)
        
        if self.jugador.tiene_escudo:
            self.pantalla.blit(self.jugador.surf_escudo, self.jugador.rect_escudo)

        for dinero in self.grupo_dinero:
            self.pantalla.blit(dinero.surf, dinero.rect)
            
        for card in self.grupo_cards:
            self.pantalla.blit(card.surf, card.rect)
            
        for escudo in self.grupo_escudos:
            self.pantalla.blit(escudo.surf, escudo.rect)

        for enemigo in self.grupo_enemigos:
            self.pantalla.blit(enemigo.surf, enemigo.rect)
            
        if self.puntuacion is not None:
            self.pantalla.blit(self.texto_puntuacion, self.rect_texto_puntuacion)
                
        if self.dificultad == 3:
            self.pantalla.blit(self.subiendo_dificultad, self.subiendo_dificultad.get_rect(center=(640, 240)))
        elif self.dificultad == 6:
            self.pantalla.blit(self.mas_dificultad, self.mas_dificultad.get_rect(center=(640, 240)))
        
        if self.i > 4800 and self.i < 5000:
            self.pantalla.blit(self.y, self.y.get_rect(center=(640, 240)))
        elif self.i > 5000 and self.i < 5150:
            self.pantalla.blit(self.chau_escudo, self.chau_escudo.get_rect(center=(640, 240)))
            self.jugador.sin_escudo()
        elif self.i > 5150 and self.i < 5300:
            pass

        if self.muerto:
            
            self.guardar_score()
            if self.puntuacion_lol > self.high_score:
                self.high_score = self.puntuacion_lol
            
            self.pantalla.fill((0, 0, 0))
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(self.sonido_gamerover)

            self.muerto = get_font(75).render("GAME OVER", True, "White")
            self.rect_muerto = self.muerto.get_rect(center=(640, 100))
            self.pantalla.blit(self.muerto, self.rect_muerto)
            
            self.high_score_texto = get_font(40).render('High Score: {:.0f}'.format(self.high_score), True, (255, 255, 255))
            self.high_score_rect = self.high_score_texto.get_rect()
            self.high_score_rect.center = (640, 350)
            
            self.texto_puntuacion_rect = self.texto_puntuacion.get_rect()
            self.texto_puntuacion_rect.center = (640, 250)
            
            self.pantalla.blit(self.texto_puntuacion, self.texto_puntuacion_rect)
            self.pantalla.blit(self.high_score_texto, self.high_score_rect)

            self.reintentar = get_font(35).render("Dale al Enter para reintentar...", True, "White")
            self.rect_reintentar = self.reintentar.get_rect()
            self.rect_reintentar.center = (640, 500)
            self.pantalla.blit(self.reintentar, self.rect_reintentar)

        pygame.display.flip()
        
    def guardar_score(self):
        high_score = self.obtener_high_score()
        
        if self.puntuacion_lol > high_score:
            high_score = self.puntuacion_lol
            
        with open("score.json", "w") as archivo:
            json.dump({"high_score": high_score}, archivo)
            
    def obtener_high_score(self):
        try:
            with open("score.json", "r") as archivo:
                datos = json.load(archivo)
                return datos["high_score"]
        except FileNotFoundError:
            return False

    def ciclo_principal(self):
        while self.ejecutando:
            tiempo = pygame.time.get_ticks()
            if self.ultimo_tiempo_frame == -1:
                tiempo_lol = 1
            else:
                tiempo_lol = tiempo - self.ultimo_tiempo_frame

            self.ultimo_tiempo_frame = tiempo
            self.actualizar(tiempo_lol)
            self.renderizar()
            self.reloj.tick(FPS)
        
            self.i += 1
            
            print(f"Dificultad: {self.dificultad}, Time: {self.i}")
            
        pygame.quit()
        
if __name__ == '__main__':
    juego = Juego()
    juego.ciclo_principal()