import pygame
import sys
from pygame.locals import *
from a_boton import Boton
from a_main import Juego

class MenuPrincipal:
    def __init__(self):
        pygame.init()

        self.pantalla = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Menú")

        self.fondo = pygame.image.load("src/sprites/otros sprites/menu.jpg")

        pygame.mixer.music.load("C:/Users/4/Desktop/pygame/src/sounds/menu.mp3")
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play(-1)

    def obtener_fuente(self, tamaño):
        return pygame.font.Font("src/fonts/font.ttf", tamaño)
    
    def opciones(self):
        while True:
            pos_mouse_op = pygame.mouse.get_pos()

            self.pantalla.fill("Gray")

            text_opt = self.obtener_fuente(25).render("There is no options menu, I lied.", True, "Black")
            rect_opt = text_opt.get_rect(center=(640, 260))
            self.pantalla.blit(text_opt, rect_opt)

            b_back = Boton(
                imagen = None,
                pos = (640, 460),
                texto = "BACK",
                fuente = self.obtener_fuente(50),
                color_base = "Black",
                color_flotante = "Green",
            )

            b_back.cambiar_color(pos_mouse_op)
            b_back.actualizar(self.pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if b_back.verificar_entrada(pos_mouse_op):
                        self.menu_principal()

            pygame.display.update()
    
    def aceptar_terminos(self):
        self.aceptado = False
        
        start_sound = pygame.mixer.Sound("src/sounds/start.mp3")
        start_sound.set_volume(0.9)
        
        b_play = Boton(
            imagen = None,
            pos = (640, 500),
            texto = "PLAY",
            fuente = self.obtener_fuente(50),
            color_base = "Black",
            color_flotante = "Green",
        )
        b_back = Boton(
            imagen = None,
            pos = (640, 600),
            texto = "BACK",
            fuente = self.obtener_fuente(50),
            color_base = "Black",
            color_flotante = "Green",
        )
        
        while True:
            self.pantalla.fill("Gray")
            pos_mouse_terminos = pygame.mouse.get_pos()

            text_ter = self.obtener_fuente(20).render("This game cannot be paused due to its difficulty.", True, "Black")
            rect_ter = text_ter.get_rect(center=(640, 260))
            self.pantalla.blit(text_ter, rect_ter)

            text_aceptar = self.obtener_fuente(20).render("If you agree to the terms, check the box below.", True, "Black")
            rect_aceptar = text_aceptar.get_rect(center=(640, 300))
            self.pantalla.blit(text_aceptar, rect_aceptar)

            if self.aceptado:
                casilla_color = "White"
            else:
                casilla_color = "Red"
                
            pygame.draw.rect(self.pantalla, casilla_color, (590, 350, 100, 100))

            if self.aceptado:
                b_play.cambiar_color(pos_mouse_terminos)
                b_play.actualizar(self.pantalla)

            b_back.cambiar_color(pos_mouse_terminos)
            b_back.actualizar(self.pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if 590 <= pos_mouse_terminos[0] <= 690 and 350 <= pos_mouse_terminos[1] <= 450:
                        self.aceptado = not self.aceptado
                    if self.aceptado and b_play.verificar_entrada(pos_mouse_terminos):
                        pygame.mixer.Sound.play(start_sound)
                        pygame.time.delay(1200)
                        juego = Juego()
                        juego.ciclo_principal()
                    if b_back.verificar_entrada(pos_mouse_terminos):
                        self.menu_principal()

            pygame.display.update()
    
    def menu_principal(self):
        flag_lol = False
        if not flag_lol:
            flag_lol = True
            self.pantalla.fill("Black")
            pygame.time.delay(1100)
        else:
            pygame.time.delay(1)

        while True:
            self.pantalla.blit(self.fondo, (0, 0))

            posicion_mouse_menu = pygame.mouse.get_pos()

            text_menu = self.obtener_fuente(60).render("SALTO SALTITO", True, "#619bd3")
            rect_menu = text_menu.get_rect(center=(640, 100))

            b_play = Boton(
                imagen = None,
                pos = (640, 250),
                texto = "PLAY",
                fuente = self.obtener_fuente(45),
                color_base = "#00e7ff",
                color_flotante = "White",
            )
            b_options = Boton(
                imagen = None,
                pos = (640, 400),
                texto = "OPTIONS",
                fuente = self.obtener_fuente(45),
                color_base = "#00e7ff",
                color_flotante = "White",
            )
            b_quit = Boton(
                imagen = None,
                pos = (640, 550),
                texto = "QUIT",
                fuente = self.obtener_fuente(45),
                color_base = "#00e7ff",
                color_flotante = "White",
            )

            self.pantalla.blit(text_menu, rect_menu)

            for b in [b_play, b_options, b_quit]:
                b.cambiar_color(posicion_mouse_menu)
                b.actualizar(self.pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if b_play.verificar_entrada(posicion_mouse_menu):
                        self.aceptar_terminos()
                    if b_options.verificar_entrada(posicion_mouse_menu):
                        self.opciones()
                    if b_quit.verificar_entrada(posicion_mouse_menu):
                        pygame.quit()
                        sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return

            pygame.display.update()
            
if __name__ == "__main__":
    menu_principal = MenuPrincipal()
    menu_principal.menu_principal()


