import pygame
from pygame.locals import *
import sqlite3
from class_boton import *

def inicializar_database():
    with sqlite3.connect("db_score.db") as conexion:
        try:
            sentencia = """
                            create table scoreboard
                            (
                                nombre text,
                                puntaje integer
                            )
                        
                        """
            conexion.execute(sentencia)
            print("Se abrio la tabla de puntuaciones")
        except sqlite3.OperationalError:
            print("La tabla ya existe")

def guardar_nuevo_puntaje(game_manager):
    with sqlite3.connect("db_score.db") as conexion:
        try:
            conexion.execute("insert into scoreboard(nombre,puntaje) values (?,?)", (game_manager.iniciales_jugador, game_manager.puntaje))
            conexion.commit()
        except:
            print("Error")


def menor_puntaje():
    with sqlite3.connect("db_score.db") as conexion:
        cursor=conexion.execute("SELECT puntaje FROM SCOREBOARD ORDER BY puntaje DESC")
        i = 0
        for fila in cursor:
            i += 1
            if i == 10:
                puntaje_mas_bajo = fila[0]
                return puntaje_mas_bajo

def mostrar_scoreboard(pantalla):
    fuente = pygame.font.Font(None, 48)
    fuente_titulo = pygame.font.Font(None, 72)
    color_texto = ("White")  

    boton_back = Boton((pantalla.get_width() // 2, pantalla.get_height() -  100),(200,50),0,"White","BACK","Black")

    with sqlite3.connect("db_score.db") as conexion:
        cursor = conexion.cursor()

        cursor.execute("SELECT nombre, puntaje FROM scoreboard ORDER BY puntaje DESC LIMIT 10")
        resultados = cursor.fetchall()

        while True:
            pantalla.fill(("Black")) 
            boton_back.update(pantalla)

            texto_titulo = fuente_titulo.render("SCOREBOARD", True, color_texto)
            pantalla.blit(texto_titulo, (pantalla.get_width()//2 - 180, 50))
            y = 150  

            for fila in resultados:
                nombre = fila[0]
                puntaje = fila[1]

                texto_nombre = fuente.render(nombre, True, color_texto)
                pantalla.blit(texto_nombre, (100, y))

                texto_puntaje = fuente.render(str(puntaje), True, color_texto)
                pantalla.blit(texto_puntaje, (pantalla.get_width()//2 + 200, y))

                y += 60 

            pygame.display.flip() 

            for event in pygame.event.get():
                if event.type == QUIT:
                    return 6
                elif event.type == MOUSEBUTTONDOWN:
                    if boton_back.rectangulo.collidepoint(event.pos):
                        return 0

