from class_jugador import *
from class_soundmanager import *

class Proyectil(GameObject):
    def __init__(self, pos_inicial, tamanio, velocidad, color, disparo_enemigo) -> None:
        super().__init__(pos_inicial, tamanio, velocidad, color)
        self.visible = False
        self.disparo_enemigo = disparo_enemigo
        if self.disparo_enemigo:
            self.orientacion_y = -1
            self.visible = True
        else:
            self.orientacion_y = 1


    def verificar_colision(self, otro_objeto):
        if self.rectangulo.colliderect(otro_objeto.rectangulo):
            self.visible = False
            self.proyectil_colisionado()
            return True

    def disparar(self, otro_objeto: Jugador, sound_manager: SoundManager, teclas = None):
        if self.disparo_enemigo:
            self.rectangulo.center = (otro_objeto.rectangulo.center[0],otro_objeto.rectangulo.center[1] + 30)
            sound_manager.disparo_enemigo.play()
        else:
            if teclas[pygame.K_SPACE]:
                self.visible = True
                self.rectangulo.center = (otro_objeto.rectangulo.center[0],otro_objeto.rectangulo.center[1] - 30)
                sound_manager.disparo_jugador.play()
        
            
    def mover_y(self, alto_pantalla):
        self.velocidad = -20
        self.rectangulo.y += self.velocidad * self.orientacion_y
        if self.rectangulo.y < -10 or self.rectangulo.y > alto_pantalla + 10:
            self.visible = False
            self.proyectil_colisionado()

    def proyectil_colisionado(self):
        self.visible = False
        self.velocidad = 0
        self.rectangulo.x = -100
        self.rectangulo.y = -100

    def update(self,pantalla,teclas,otro_objeto,sound_manager):
        if not self.visible:
            self.disparar(otro_objeto,sound_manager,teclas)
        else:
            self.mover_y(pantalla.get_height())

        if self.visible:
            super().update(pantalla)
