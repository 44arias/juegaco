class Boton:
    def __init__(self, imagen, pos, texto, fuente, color_base, color_flotante):
        self.imagen = imagen
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.fuente = fuente
        self.color_base, self.color_flotante = color_base, color_flotante
        self.texto = texto
        self.texto_renderizado = self.fuente.render(self.texto, True, self.color_base)
        if self.imagen is None:
            self.imagen = self.texto_renderizado
        self.rectangulo = self.imagen.get_rect(center=(self.x_pos, self.y_pos))
        self.rectangulo_texto = self.texto_renderizado.get_rect(center=(self.x_pos, self.y_pos))
        self.activado = False

    def actualizar(self, pantalla):
        if self.imagen is not None:
            pantalla.blit(self.imagen, self.rectangulo)
        pantalla.blit(self.texto_renderizado, self.rectangulo_texto)

    def verificar_entrada(self, posicion):
        if posicion[0] in range(self.rectangulo.left, self.rectangulo.right) and posicion[1] in range(self.rectangulo.top, self.rectangulo.bottom):
            return True
        return False

    def cambiar_color(self, posicion):
        if posicion[0] in range(self.rectangulo.left, self.rectangulo.right) and posicion[1] in range(self.rectangulo.top, self.rectangulo.bottom):
            self.texto_renderizado = self.fuente.render(self.texto, True, self.color_flotante)
        else:
            self.texto_renderizado = self.fuente.render(self.texto, True, self.color_base)

    def activar(self):
        self.activado = True

    def desactivar(self):
        self.activado = False