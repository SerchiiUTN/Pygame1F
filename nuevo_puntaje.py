import pygame
from pygame.locals import *
from class_boton import *
from scoreboard import *


def nuevo_puntaje(game_manager,pantalla):
    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    cursor_posiciones = [0, 0, 0]
    letras_seleccionadas = [letras[pos] for pos in cursor_posiciones]
    posicion_i = 0

    boton_save = Boton((pantalla.get_width() // 2, pantalla.get_height() -  250),(200,50),0,"White","SAVE SCORE","Black")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 6
            elif event.type == MOUSEBUTTONDOWN:
                if boton_save.rectangulo.collidepoint(event.pos):
                    iniciales = ""
                    iniciales = iniciales.join(letras_seleccionadas)
                    game_manager.iniciales_jugador = iniciales
                    guardar_nuevo_puntaje(game_manager)
                    return 0
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    posicion_i -= 1
                    if posicion_i < 0:
                        posicion_i = len(cursor_posiciones) - 1
                elif event.key == K_RIGHT:
                    posicion_i += 1
                    if posicion_i >= len(cursor_posiciones):
                        posicion_i = 0
                elif event.key == K_UP:
                    cursor_posiciones[posicion_i] += 1
                    if cursor_posiciones[posicion_i] >= len(letras):
                        cursor_posiciones[posicion_i] = 0
                elif event.key == K_DOWN:
                    cursor_posiciones[posicion_i] -= 1
                    if cursor_posiciones[posicion_i] < 0:
                        cursor_posiciones[posicion_i] = len(letras) - 1

                letras_seleccionadas[posicion_i] = letras[cursor_posiciones[posicion_i]]

        pantalla.fill((0, 0, 0))
        boton_save.update(pantalla)
        
        font = pygame.font.Font(None, 72)
        texto_titulo = font.render("NEW RECORD", True, (255, 255, 255))
        pantalla.blit(texto_titulo, (pantalla.get_width() // 2 -170, 100))
        texto_score = font.render("SCORE: "+ str(game_manager.puntaje), True, (255, 255, 255))
        pantalla.blit(texto_score, (pantalla.get_width() // 2 -140, 240))
        for i in range(3):
            texto = font.render(letras_seleccionadas[i], True, (255, 255, 255))
            texto_rect = texto.get_rect(center=(pantalla.get_width() // 2 + (i - 1) * 100, pantalla.get_height() // 2))
            pantalla.blit(texto, texto_rect)
            if posicion_i == i:
                pygame.draw.rect(pantalla, "White", (texto_rect.x - 5, texto_rect.y + 50 , 50, 5))

        pygame.display.flip()