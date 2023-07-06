import pygame
from pygame.sprite import Sprite

class GameObject(Sprite):
    def __init__(self, pos_inicial, tamanio, velocidad, color) -> None:
        super().__init__()
        self.surface = pygame.Surface(tamanio)
        self.surface.fill(color)

        self.rectangulo = self.surface.get_rect()

        self.rectangulo.center = pos_inicial

        self.velocidad = velocidad


    def draw(self, pantalla):
        pantalla.blit(self.surface,self.rectangulo)

    def update(self, pantalla):
        self.draw(pantalla)
