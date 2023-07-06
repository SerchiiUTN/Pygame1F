from class_gameobject import *

class Barrera(GameObject):
    def __init__(self, pos_inicial, tamanio, color):
        super().__init__(pos_inicial, tamanio, 0, color)
        self.visible = True
