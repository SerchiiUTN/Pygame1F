#import pygame
from pygame.locals import *
import sys
from class_gamemanager import *
from class_soundmanager import *
from class_jugador import *
from class_proyectil import *
from class_barrera import *
from funciones import *
from class_boton import *
from sprites import *

#start
def nivel_1(game_manager, sound_manager, pantalla, velocidad_enemigo):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    RELOJ = pygame.time.Clock()
    FPS = 60

    reescalar_imagen(personaje_sprite,(30,30))
    reescalar_imagen(enemigo_sprite,(30,30))

    jugador = Jugador((pantalla.get_width()/2,pantalla.get_height()-30),(30,30),5,"White", pygame.K_LEFT, pygame.K_RIGHT,game_manager.vidas_jugador, personaje_sprite)
    proyectil_jugador = Proyectil((-100,-100),(5,30),0,"White", False)
    fondo_mensaje = Boton((pantalla.get_width()/2,pantalla.get_height()/2 ),(200,50),0,"Black","","White")
    

    listado_barreras = []

    fortaleza_pos_x = 50

    crear_fortaleza(fortaleza_pos_x,listado_barreras)

    matriz_enemigos = []
    disparos_enemigos = []

    game_manager.cantidad_enemigos = crear_colmena(matriz_enemigos,velocidad_enemigo)


    #update
    while True:
        RELOJ.tick(FPS)
        delta_time = RELOJ.tick(FPS) / 1000

        teclas_presionadas = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                return 6

        if not jugador.con_vida or game_manager.cantidad_enemigos <= 0 or game_manager.enemigo_en_base:
            game_manager.juego_activo = False

            
        if game_manager.juego_activo:
            pantalla.fill("Black")
            game_manager.update()
            pantalla.blit(game_manager.text_puntaje, (10, 10))
            pantalla.blit(game_manager.text_vidas, (pantalla.get_width()-80,10))
            pantalla.blit(game_manager.text_nivel,(pantalla.get_width()/2-30,10))

            jugador.update(pantalla, teclas_presionadas,disparos_enemigos,sound_manager)
            proyectil_jugador.update(pantalla, teclas_presionadas, jugador, sound_manager)
            comportamiento_colmena(matriz_enemigos,pantalla,proyectil_jugador,game_manager,sound_manager,delta_time,disparos_enemigos)

            for proyectil in disparos_enemigos:
                proyectil.update(pantalla, teclas_presionadas, jugador, sound_manager)

                if proyectil.rectangulo.y > pantalla.get_height()-10 or not proyectil.visible:
                    disparos_enemigos.remove(proyectil)

                comportamiento_barreras(listado_barreras,pantalla,proyectil)

            comportamiento_barreras(listado_barreras,pantalla,proyectil_jugador)
            pygame.display.flip()
        else:
            game_manager.update()
            pantalla.blit(game_manager.text_puntaje, (10, 10))
            pantalla.blit(game_manager.text_vidas, (pantalla.get_width()-80,10))
            pantalla.blit(game_manager.text_nivel,(pantalla.get_width()/2-30,10))
            fondo_mensaje.update(pantalla)
            if not jugador.con_vida or game_manager.enemigo_en_base:
                if game_manager.vidas_jugador > 1 and not game_manager.enemigo_en_base:  
                    game_manager.vidas_jugador = game_manager.vidas_jugador - 1
                    game_manager.update()
                    pantalla.blit(game_manager.mensaje_vida_perdida,(pantalla.get_width()/2-100,pantalla.get_height()/2))
                    jugador.con_vida = True
                    game_manager.juego_activo = True
                    pygame.display.flip()
                    pygame.time.delay(3000)
                else:
                    pantalla.blit(game_manager.mensaje_game_over,(pantalla.get_width()/2-50,pantalla.get_height()/2))
                    pygame.display.flip()
                    jugador.con_vida = True
                    game_manager.juego_activo = True
                    game_manager.enemigo_en_base = False
                    pygame.time.delay(3000)
                    return 4
            elif game_manager.cantidad_enemigos <= 0:
                if game_manager.nivel < 3:
                    pantalla.blit(game_manager.mensaje_siguiente_nivel,(pantalla.get_width()/2-100,pantalla.get_height()/2))
                else:
                    pantalla.blit(game_manager.mensaje_ganaste,(pantalla.get_width()/2-30,pantalla.get_height()/2))
                
                pygame.display.flip()
                pygame.time.delay(3000)
                return game_manager.nivel + 1
            
