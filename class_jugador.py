from class_gameobject import *
from sprites import *

class Jugador(GameObject):
    def __init__(self, pos_inicial, tamanio, velocidad, color, izquierda, derecha, vidas, sprites) -> None:
        super().__init__(pos_inicial, tamanio, velocidad, color)
        self.sprites = sprites
        self.surface = self.sprites[0]
        self.tecla_izq = izquierda
        self.tecla_der = derecha
        self.vidas = vidas
        self.con_vida = True

    def mover_y(self, ancho_pantalla, teclas):
        if teclas[self.tecla_izq]:
            self.velocidad = -5
        elif teclas[self.tecla_der]:
            self.velocidad = 5
        else:
            self.velocidad = 0

        if self.rectangulo.right > ancho_pantalla-10:
            self.rectangulo.right = ancho_pantalla-10
        elif self.rectangulo.left < 10:
            self.rectangulo.left = 10

        self.rectangulo.x += self.velocidad

    def update(self,pantalla,teclas,disparos,sound_manager):
        self.mover_y(pantalla.get_width(),teclas)
        self.verificar_colision(disparos,sound_manager)
        if self.con_vida:
            self.surface = self.sprites[0]
        else:
            self.surface = self.sprites[1]
        super().update(pantalla)


    def verificar_colision(self,disparos: list,sound_manager):
        for disparo in disparos:
            if self.rectangulo.colliderect(disparo.rectangulo):
                disparo.proyectil_colisionado()
                sound_manager.explosion_jugador.play()
                self.con_vida = False
