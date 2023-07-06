from class_gameobject import *
from class_proyectil import *

class Enemigo(GameObject):
    def __init__(self, pos_inicial, tamanio, velocidad, color, puntaje, tiempo_movimiento, sprite) -> None:
        super().__init__(pos_inicial, tamanio, velocidad, color)
        self.surface = sprite
        self.tiempo_movimiento = tiempo_movimiento
        self.tiempo_inicial = 0
        self.puntaje = puntaje

    def cambiar_direccion(self,posicion):
        self.rectangulo.x = self.rectangulo.x + posicion
        self.rectangulo.y = self.rectangulo.y + 30
        self.velocidad *= -1
        self.cambiar_velocidad(0.0001)

    def movimiento(self,delta_time):
        self.tiempo_inicial = self.tiempo_inicial + delta_time

        if self.tiempo_inicial > self.tiempo_movimiento:
            self.rectangulo.x += self.velocidad
            self.tiempo_inicial = 0

    def cambiar_velocidad(self,velocidad):
        self.tiempo_movimiento = self.tiempo_movimiento - velocidad

    def update(self,pantalla,delta_time):
        self.movimiento(delta_time)
        super().update(pantalla)

    def disparar(self, proyectiles_enemigos, sound_manager):
        proyectil = Proyectil((-100, -100), (5, 30), -20, "Red", True)
        proyectil.disparar(self,sound_manager)
        proyectiles_enemigos.append(proyectil)
