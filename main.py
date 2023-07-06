import pygame
import sys
from pygame.locals import *
from class_boton import *
from menu_principal import *
from nivel_1 import *
from class_gamemanager import *
from class_soundmanager import *
from nuevo_puntaje import *
from scoreboard import *



def main():
    pygame.init()

    #Ventana principal
    ANCHO_PANTALLA = 750
    ALTO_PANTALLA = 900
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption('Menú Principal')

    
    game_manager = GameManager(True,0,3,0)
    sound_manager = SoundManager(pygame.mixer.Sound("sounds\\DisparoJugador.wav"),pygame.mixer.Sound("sounds\\DisparoEnemigo.wav"),pygame.mixer.Sound("sounds\\ExplosionJugador.wav"),pygame.mixer.Sound("sounds\\ExplosionEnemigo.wav"),[pygame.mixer.Sound("sounds\\Paso1.wav"),pygame.mixer.Sound("sounds\\Paso2.wav"),pygame.mixer.Sound("sounds\\Paso3.wav"),pygame.mixer.Sound("sounds\\Paso4.wav")])

    inicializar_database()

    nivel = 0

    while nivel != -1:
        match nivel:
            case 0:
                nivel = mostrar_menu_principal(pantalla)
            case 1:
                game_manager.nivel = nivel
                game_manager.puntaje = 0
                game_manager.vidas_jugador = 3
                game_manager.juego_activo = True
                nivel = nivel_1(game_manager,sound_manager,pantalla,0.9)
            case 2:
                game_manager.nivel = nivel
                game_manager.juego_activo = True
                nivel = nivel_1(game_manager,sound_manager,pantalla,0.7)
            case 3:
                game_manager.nivel = nivel
                game_manager.juego_activo = True
                nivel = nivel_1(game_manager,sound_manager,pantalla,0.5)
            case 4:
                puntaje_mas_bajo = menor_puntaje()
                if game_manager.puntaje > puntaje_mas_bajo: 
                    nivel = nuevo_puntaje(game_manager,pantalla)
                else:
                    nivel = 0
            case 5:
                nivel = mostrar_scoreboard(pantalla)
            case 6:
                print("Se cierra el juego")
                pygame.quit()
                sys.exit()



main()
            