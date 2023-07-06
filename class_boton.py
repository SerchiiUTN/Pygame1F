from class_gameobject import *

class Boton(GameObject):
    def __init__(self, pos_inicial, tamanio, velocidad, color, texto, color_texto) -> None:
        super().__init__(pos_inicial, tamanio, velocidad, color)
        self.fuente = pygame.font.SysFont(None, 36)
        self.texto = self.fuente.render(texto, True, color_texto)
        self.texto_rect = self.texto.get_rect()
        self.texto_rect.center = self.rectangulo.center


    def draw(self, pantalla):
        super().draw(pantalla)
        pantalla.blit(self.texto, self.texto_rect)

    

