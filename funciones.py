from class_gamemanager import *
from class_soundmanager import *
from class_jugador import *
from class_proyectil import *
from class_barrera import *
from class_enemigo import *
from sprites import *
import random
from copy import deepcopy

#Funciones colmena
def comportamiento_colmena(colmena:list[list],pantalla,proyectil_jugador: Proyectil, game_manager: GameManager, sound_manager: SoundManager, delta_time,disparos):
    colision_bordes = False
    colision_enemigo = False
    acomodar_enemigo = 0
    tiempo_disparo = 1
    game_manager.timer_disparo_enemigo = game_manager.timer_disparo_enemigo + delta_time
    index_enemigo = 0

    if game_manager.cantidad_enemigos > 0:
        disparo_random = random.randint(1,game_manager.cantidad_enemigos)

    for columna in colmena:
        for enemigo in columna:
            index_enemigo = index_enemigo + 1
            
            if enemigo.rectangulo.right > pantalla.get_width() or enemigo.rectangulo.left < 10:
                acomodar_enemigo = enemigo.velocidad * -1
                colision_bordes = True
                break

            if game_manager.timer_disparo_enemigo > tiempo_disparo and index_enemigo == disparo_random:
                enemigo.disparar(disparos,sound_manager)
                game_manager.timer_disparo_enemigo = 0

            if proyectil_jugador.verificar_colision(enemigo):
                game_manager.puntaje = game_manager.puntaje + enemigo.puntaje
                columna.remove(enemigo)
                game_manager.cantidad_enemigos = game_manager.cantidad_enemigos - 1
                sound_manager.explosion_enemigo.play()
                colision_enemigo = True

            if enemigo.rectangulo.y >= pantalla.get_height()-60:
                sound_manager.explosion_jugador.play()
                game_manager.enemigo_en_base = True
                
        
        if colision_bordes:
            break
    
    if colision_bordes:
        for columna in colmena:
            for enemigo in columna:
                enemigo.cambiar_direccion(acomodar_enemigo)

    if colision_enemigo:
        for columna in colmena:
            for enemigo in columna:
                enemigo.cambiar_velocidad(0.018)

    for columna in colmena:
        for enemigo in columna:
            sound_manager.timer_movimiento = enemigo.tiempo_inicial
            sound_manager.tiempo_movimiento = enemigo.tiempo_movimiento
            
            enemigo.update(pantalla,delta_time)
            
    sound_manager.update(delta_time)
    
def crear_colmena(colmena: list, velocidad_enemigo) -> int:
    enemy_pos_x = 30
    cantidad_enemigos = 0
    
    puntaje = 0
    for columna in range(11):
        enemy_pos_y = 60
        columna_enemigos = []
        index_fila = 0
        for enemigo in range(5):
            index_fila = index_fila + 1
            if index_fila == 1:
                puntaje = 30
                sprite_enemigo = enemigo_sprite[2]
            elif index_fila == 2 or index_fila == 3:
                puntaje = 20
                sprite_enemigo = enemigo_sprite[1]
            else:
                puntaje = 10
                sprite_enemigo = enemigo_sprite[0]
            enemigo = Enemigo((enemy_pos_x,enemy_pos_y),(30,30),15,"Green",puntaje,velocidad_enemigo,sprite_enemigo)
            enemy_pos_y = enemy_pos_y + 60
            columna_enemigos.append(enemigo)
            cantidad_enemigos = cantidad_enemigos +1
        colmena.append(columna_enemigos)

        enemy_pos_x = enemy_pos_x + 60
    
    return cantidad_enemigos
    
#Funciones barreras
def crear_barrera(pos_x,pos_y,barrera):
    barrera_pos_x = pos_x
    for columna_barrera in range(4):
        barrera_pos_y = pos_y
        columna_barrera = []
        for elemento in range(4):
            elemento = Barrera((barrera_pos_x,barrera_pos_y),(30,30),"Orange")
            barrera_pos_y = barrera_pos_y + 30
            columna_barrera.append(elemento)
        barrera.append(columna_barrera)

        barrera_pos_x = barrera_pos_x + 30

def crear_fortaleza(fortaleza_pos_x,listado_barreras):
    for fortaleza in range(4):
        fortaleza = []
        crear_barrera(fortaleza_pos_x,690,fortaleza)

        listado_barreras.append(fortaleza)
        fortaleza_pos_x = fortaleza_pos_x + 180

def comportamiento_barreras(listado_barreras,pantalla,proyectil):
    for fortaleza in listado_barreras:
        for barrera in fortaleza:
            for elemento in barrera:
                elemento.update(pantalla)
                if proyectil.verificar_colision(elemento):
                    elemento.visible = False
                
                if not elemento.visible:
                    barrera.remove(elemento)
