

class SoundManager():
    def __init__(self,disparo_jugador,disparo_enemigo,explosion_jugador,explosion_enemigo,movimiento_enemigo: list) -> None:
        self.disparo_jugador = disparo_jugador
        self.disparo_enemigo = disparo_enemigo
        self.explosion_jugador = explosion_jugador
        self.explosion_enemigo = explosion_enemigo
        self.movimiento_enemigo = movimiento_enemigo
        self.index_movimiento_enemigo = 0
        self.tiempo_movimiento = 1
        self.timer_movimiento = 0

    def reproduce_movimiento_enemigo(self):
            self.movimiento_enemigo[self.index_movimiento_enemigo].play()
            self.index_movimiento_enemigo = self.index_movimiento_enemigo + 1
            if self.index_movimiento_enemigo >= 4:
                self.index_movimiento_enemigo = 0

    def update(self,delta_time):

        self.timer_movimiento = self.timer_movimiento + delta_time

        if self.timer_movimiento > self.tiempo_movimiento:
            self.reproduce_movimiento_enemigo()
            self.timer_movimiento = 0
