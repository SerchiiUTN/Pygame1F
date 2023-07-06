import pygame
import sys
from pygame.locals import *
from class_boton import *
from sprites import *

pygame.init()



def mostrar_menu_principal(pantalla):

    reescalar_imagen(titulo_sprite,(640 , 269))
    titulo_imagen = titulo_sprite[0]

    titulo_x = (pantalla.get_width() - titulo_imagen.get_width()) // 2
    titulo_y = pantalla.get_height() // 2 - titulo_imagen.get_height() - 100


    while True:
        pantalla.fill("Black")  

        boton_iniciar = Boton((pantalla.get_width() // 2, pantalla.get_height() - 400),(200,50),0,"White","PLAY","Black") 
        boton_scoreboard = Boton((pantalla.get_width() // 2, pantalla.get_height() - 300),(200,50),0,"White","SCOREBOARD","Black")
        boton_quit = Boton((pantalla.get_width() // 2, pantalla.get_height() -  200),(200,50),0,"White","QUIT","Black")
        
        pantalla.blit(titulo_imagen, (titulo_x, titulo_y))
        boton_iniciar.update(pantalla)
        boton_scoreboard.update(pantalla)
        boton_quit.update(pantalla)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == QUIT:
                return 6
                
            elif evento.type == MOUSEBUTTONDOWN:
                if boton_iniciar.rectangulo.collidepoint(evento.pos):
                    return 1
                elif boton_scoreboard.rectangulo.collidepoint(evento.pos):
                    return 5
                elif boton_quit.rectangulo.collidepoint(evento.pos):
                    return 6
