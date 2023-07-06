import pygame
from class_boton import *

class GameManager():
    def __init__(self,juego_activo,puntaje,vidas_jugador,cantidad_enemigos, nivel= 0) -> None:
        self.juego_activo = juego_activo
        self.vidas_jugador = vidas_jugador
        self.cantidad_enemigos = cantidad_enemigos
        self.puntaje = puntaje
        self.timer_disparo_enemigo = 0
        self.jugador_eliminado = False
        self.mensaje_fuente = pygame.font.SysFont("Helvetica", 20)
        self.mensaje_vida_perdida = self.mensaje_fuente.render("Te dieron. Te quedan "+str(self.vidas_jugador)+" vidas", True, "White")
        self.mensaje_game_over = self.mensaje_fuente.render("Game Over", True, "White")
        self.mensaje_siguiente_nivel = self.mensaje_fuente.render("Pasas al siguiente nivel", True, "White")
        self.mensaje_ganaste = self.mensaje_fuente.render("Ganaste", True, "White")
        self.text_puntaje = ""
        self.text_vidas = ""
        self.text_nivel = ""
        self.nivel = nivel
        self.iniciales_jugador = ""
        self.enemigo_en_base = False

    def update(self):
        self.text_puntaje = self.mensaje_fuente.render("SCORE: " + str(self.puntaje), True, "White")
        self.text_vidas = self.mensaje_fuente.render("LIVES: "+ str(self.vidas_jugador), True, "White")
        self.text_nivel = self.mensaje_fuente.render("LEVEL: "+str(self.nivel), True, "White")
        self.mensaje_vida_perdida = self.mensaje_fuente.render("Te dieron. Te quedan "+str(self.vidas_jugador)+" vidas", True, "White")

        