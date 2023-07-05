import pygame
from pygame.locals import *
from a_config import *

class Jugador(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Jugador, self).__init__()

        self.animacion_actual = 'run'
        self.animaciones = {}
        self.comportamiento_animaciones = {
            'run': 'todo_el_tiempo',
            'jump': 'una_vez',
            'doublejump': 'una_vez',
        }

        self.cargar_assets()

        self.indice_animacion = 0
        self.velocidad_animacion = 0.16
        self.pausado = False

        self.surf = self.animaciones[self.animacion_actual][self.indice_animacion]
        self.surf = pygame.transform.scale(self.surf, (ANCHO_2, ALTURA_2))
        self.rect = self.surf.get_rect()

        self.hitbox = pygame.Rect(0, 0, self.rect.width, self.rect.height)

        self.posicion = pygame.math.Vector2(100, 300)

        self.velocidad = pygame.math.Vector2(0, 0)
        self.aceleracion = pygame.math.Vector2(0, 0.022)

        self.contador_saltos = 0
        self.puede_saltar = False
        self.realizar_salto = False
        self.va_a_saltar = False
        self.tiempo_ta_por_saltar = -1
        self.ultimo_salto = pygame.time.get_ticks()
        self.salto_lol = 100
        self.muerto = False
        self.sumar_puntuacion = 0
        self.toca_suelo = False
        self.flag_rara = True
                
        self.tiene_escudo = True
        self.surf_escudo = pygame.image.load("src/sprites/pickups/escudogrande.png")
        self.surf_escudo = pygame.transform.scale(self.surf_escudo, (ANCHO_2 * 1.1, ALTURA_2 * 1.1))
        self.rect_escudo = self.surf_escudo.get_rect()

        # self.solo_puede_saltar_hacia_abajo = False
        
        self.sonido_hurt = pygame.mixer.Sound("src/sounds/hurt.mp3")
        self.sonido_hurt.set_volume(.1)
        self.sonido_dinero = pygame.mixer.Sound("src/sounds/dinero.mp3")
        self.sonido_dinero.set_volume(.1)
        self.sonido_card = pygame.mixer.Sound("src/sounds/card.mp3")
        self.sonido_card.set_volume(.1)
        self.sonido_escudo = pygame.mixer.Sound("src/sounds/escudo.mp3")
        self.sonido_escudo.set_volume(.1)

    def cargar_animacion(self, nombre):
        self.animaciones[nombre] = []
        
        asset = pygame.image.load(f"src/sprites/cyborg/Cyborg_{nombre}.png").convert_alpha()
        ancho = asset.get_width()
        indice = 0

        while indice * TAMAÑO_ASSET < ancho:
            frame = pygame.Surface((TAMAÑO_ASSET, TAMAÑO_ASSET), pygame.SRCALPHA)
            frame.blit(asset, asset.get_rect(), Rect(indice * TAMAÑO_ASSET, 0, TAMAÑO_ASSET, TAMAÑO_ASSET))
            self.animaciones[nombre].append(frame)
            indice += 1

    def cargar_assets(self):
        self.cargar_animacion('run')
        self.cargar_animacion('jump')
        self.cargar_animacion('doublejump')
        self.cargar_animacion('hurt')

    def cambiar_animacion(self, nombre):
        if self.animacion_actual != nombre:
            self.animacion_actual = nombre
            self.indice_animacion = 0

    def saltar(self):
        if pygame.time.get_ticks() - self.ultimo_salto < 100:
            return
        self.ultimo_salto = pygame.time.get_ticks()

        if self.puede_saltar:
            self.realizar_salto = True
            self.va_a_saltar = False
            if self.contador_saltos == 2:
                self.puede_saltar = False
        else:
            self.va_a_saltar = True
            self.tiempo_ta_por_saltar = pygame.time.get_ticks()

    def cancelar_salto(self):
        if self.velocidad.y < -3:
            self.velocidad.y = -3

    def comprobar_colisiones_suelo(self, grupo_sprites):
        antiguo_rect = self.rect
        self.rect = self.hitbox
        colisiones = pygame.sprite.spritecollide(self, grupo_sprites, False)
        self.rect = antiguo_rect
        self.colisionando_con_suelo = False

        if colisiones:
            if self.rect.bottom - colisiones[0].rect.top < (TAMAÑO_ASSET / 2) and self.velocidad.y >= 0:
                self.velocidad.y = 0
                self.contador_saltos = 0
                self.puede_saltar = True
                self.posicion.y = colisiones[0].rect.top + 1
                self.cambiar_animacion('run')
                if self.va_a_saltar:
                    self.saltar()
                self.colisionando_con_suelo = True
        else:
            if self.contador_saltos == 2:
                self.puede_saltar = False

    def comprobar_colisiones_enemigos(self, grupo):
        colisiones = pygame.sprite.spritecollide(self, grupo, False, pygame.sprite.collide_mask)
        if colisiones:
            if self.tiene_escudo:
                self.tiene_escudo = False
                colisiones[0].kill()
                self.cambiar_animacion('hurt')
                pygame.mixer.Sound.play(self.sonido_hurt)                
            else:
                self.muerto = True
                
    def comprobar_colisiones_escudos(self, grupo):
        antiguo_rect = self.rect
        self.rect = self.hitbox
        colisiones = pygame.sprite.spritecollide(self, grupo, True, pygame.sprite.collide_rect_ratio(1))
        self.rect = antiguo_rect
        if colisiones:
            for colision in colisiones:
                self.tiene_escudo = True
                self.sumar_puntuacion += 100
                colision.kill()
                pygame.mixer.Sound.play(self.sonido_escudo)

    def comprobar_colisiones_pickups(self, grupo, puntos, tipo):
        antiguo_rect = self.rect
        self.rect = self.hitbox
        colisiones = pygame.sprite.spritecollide(self, grupo, True, pygame.sprite.collide_rect_ratio(1))
        self.rect = antiguo_rect
        if colisiones:
            for colision in colisiones:
                if tipo == 'dinero':
                    self.sumar_puntuacion += puntos
                    pygame.mixer.Sound.play(self.sonido_dinero)
                    colision.kill()
                else:
                    self.sumar_puntuacion += puntos
                    pygame.mixer.Sound.play(self.sonido_card)
                    colision.kill()
                    
    def animar(self, tiempo_lol): 
        self.velocidad_animacion = 0.008 * tiempo_lol
        self.indice_animacion += self.velocidad_animacion
        
        if self.animacion_actual == 'hurt':
            if int(self.indice_animacion) >= len(self.animaciones[self.animacion_actual]):
                self.cambiar_animacion('run')
        else:
            if int(self.indice_animacion) + 1 >= len(self.animaciones[self.animacion_actual]):
                if self.comportamiento_animaciones[self.animacion_actual] == 'todo_el_tiempo':
                    self.indice_animacion = 0
                else:
                    self.indice_animacion = len(self.animaciones[self.animacion_actual]) - 1
                
        self.surf = self.animaciones[self.animacion_actual][int(self.indice_animacion)]
        self.surf = pygame.transform.scale(self.surf, (ANCHO_2, ALTURA_2))
        self.rect = self.surf.get_rect()

        self.actualizar_hitbox()
        self.actualizar_mask()

    def actualizar(self, tiempo_lol, grupo_colision_suelo, grupo_dinero, grupo_card, grupo_escudo, grupo_enemigos):
        if self.pausado:
            return
        
        self.comprobar_colisiones_suelo(grupo_colision_suelo)
        self.comprobar_colisiones_pickups(grupo_dinero, 50, 'dinero')
        self.comprobar_colisiones_pickups(grupo_card, 350, 'card')
        self.comprobar_colisiones_escudos(grupo_escudo)
        self.comprobar_colisiones_enemigos(grupo_enemigos)

        if self.muerto:
            return

        self.animar(tiempo_lol)

        ahora = pygame.time.get_ticks()

        if self.va_a_saltar and ahora - self.tiempo_ta_por_saltar > self.salto_lol:
            self.va_a_saltar = False

        if self.realizar_salto:
            if self.contador_saltos == 0 and not self.colisionando_con_suelo:
                self.contador_saltos += 1

            if self.contador_saltos == 0:
                self.velocidad.y = FUERZA_SALTO * -1
                self.cambiar_animacion('jump')
            elif self.contador_saltos == 1:
                self.velocidad.y = FUERZA_SALTO * -1 * 0.8
                self.cambiar_animacion('doublejump')
            self.contador_saltos += 1
            self.realizar_salto = False

        self.velocidad += self.aceleracion * tiempo_lol
        self.posicion += self.velocidad

        if self.rect.top > ALTURA:
            if self.tiene_escudo:
                self.tiene_escudo = False
                self.posicion.y = 50
            else:
                self.muerto = True

        self.rect.midbottom = self.posicion
        self.actualizar_hitbox()
        self.actualizar_mask()
        self.actualizar_escudo()

        # if self.solo_puede_saltar_hacia_abajo and self.velocidad.y > 0:
        #     self.solo_puede_saltar_hacia_abajo = False
            
    def sin_escudo(self):
        if self.flag_rara and self.tiene_escudo:
            self.tiene_escudo = False
            self.cambiar_animacion('hurt')
            pygame.mixer.Sound.play(self.sonido_hurt) 
            self.flag_rara = False  

    def guardar_con_escudo(self):
        if self.tiene_escudo:
            self.tiene_escudo = False
            self.solo_saltar_hacia_abajo = True
            self.velocidad.y = FUERZA_SALTO * - 1.5
            self.posicion.y -= 20
            self.contador_saltos = 0
            self.puede_saltar = True
            self.cambiar_animacion('jump')
        else:
            self.muerto = True

    def actualizar_escudo(self):
        self.rect_escudo.center = (
            self.rect.center[0] - 20,
            self.rect.center[1] + 10,
        )

    def actualizar_hitbox(self):        
        self.hitbox = pygame.Rect(
            self.rect.x + 20,
            self.rect.y,
            self.rect.width - 20,
            self.rect.height
        )

    def actualizar_mask(self):
        self.mask_surf = self.surf
        self.mask_surf = pygame.transform.scale(self.mask_surf, (ANCHO_2 * 0.8, ALTURA_2 * 0.8))
        self.mask = pygame.mask.from_surface(self.mask_surf)