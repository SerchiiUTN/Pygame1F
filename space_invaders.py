import pygame
import random
from copy import deepcopy
from pygame.locals import *
import sys

class GameObject:
    def __init__(self, pos_inicial, tamanio, velocidad, color) -> None:
        self.surface = pygame.Surface(tamanio)
        self.surface.fill(color)

        self.rectangulo = self.surface.get_rect()

        self.rectangulo.center = pos_inicial

        self.velocidad = velocidad


    def draw(self, pantalla):
        pantalla.blit(self.surface,self.rectangulo)

    def update(self, pantalla):
        self.draw(pantalla)

class GameManager():
    def __init__(self,juego_activo,puntaje,vidas_jugador,cantidad_enemigos) -> None:
        self.juego_activo = juego_activo
        self.vidas_jugador = vidas_jugador
        self.cantidad_enemigos = cantidad_enemigos
        self.puntaje = puntaje
        self.timer_disparo_enemigo = 0
        self.jugador_eliminado = False
        self.mensaje_fuente = pygame.font.SysFont('Helvetica', 20)
        self.mensaje_vida_perdida = self.mensaje_fuente.render("Perdiste una vida", True, "White")
        self.mensaje_game_over = self.mensaje_fuente.render("Game Over", True, "White")
        self.mensaje_siguiente_nivel = self.mensaje_fuente.render("Pasas al siguiente nivel", True, "White")
        self.mensaje_ganaste = self.mensaje_fuente.render("Ganaste", True, "White")
        self.text_puntaje = ""


    def update(self):
        self.text_puntaje = self.mensaje_fuente.render("SCORE: " + str(self.puntaje), True, "White")

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

class Jugador(GameObject):
    def __init__(self, pos_inicial, tamanio, velocidad, color, izquierda, derecha, vidas) -> None:
        super().__init__(pos_inicial, tamanio, velocidad, color)
        self.tecla_izq = izquierda
        self.tecla_der = derecha
        self.vidas = vidas
        self.con_vida = True

    def mover_y(self, ancho_pantalla, teclas):
        if teclas[self.tecla_izq]:
            self.velocidad = -5
        elif teclas[self.tecla_der]:
            self.velocidad = 5
        else:
            self.velocidad = 0

        if self.rectangulo.right > ancho_pantalla-10:
            self.rectangulo.right = ancho_pantalla-10
        elif self.rectangulo.left < 10:
            self.rectangulo.left = 10

        self.rectangulo.x += self.velocidad

    def update(self,pantalla,teclas,disparos,sound_manager):
        self.mover_y(pantalla.get_width(),teclas)
        self.verificar_colision(disparos,sound_manager)
        super().update(pantalla)


    def verificar_colision(self,disparos: list,sound_manager):
        for disparo in disparos:
            if self.rectangulo.colliderect(disparo.rectangulo):
                disparo.proyectil_colisionado()
                sound_manager.explosion_jugador.play()
                self.con_vida = False

class Enemigo(GameObject):
    def __init__(self, pos_inicial, tamanio, velocidad, color, puntaje) -> None:
        super().__init__(pos_inicial, tamanio, velocidad, color)
        self.tiempo_movimiento = 0.9
        self.tiempo_inicial = 0
        self.puntaje = puntaje

    def cambiar_direccion(self,posicion):
        self.rectangulo.x = self.rectangulo.x + posicion
        self.rectangulo.y = self.rectangulo.y + 30
        self.velocidad *= -1
        self.cambiar_velocidad(0.0001)

    def movimiento(self,delta_time):
        self.tiempo_inicial = self.tiempo_inicial + delta_time

        if self.tiempo_inicial > self.tiempo_movimiento:
            self.rectangulo.x += self.velocidad
            self.tiempo_inicial = 0

    def cambiar_velocidad(self,velocidad):
        self.tiempo_movimiento = self.tiempo_movimiento - velocidad

    def update(self,pantalla,delta_time):
        self.movimiento(delta_time)
        super().update(pantalla)

    def disparar(self, proyectiles_enemigos, sound_manager):
        proyectil = Proyectil((-100, -100), (5, 30), -20, "Red", True)
        proyectil.disparar(self,sound_manager)
        proyectiles_enemigos.append(proyectil)

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

class Barrera(GameObject):
    def __init__(self, pos_inicial, tamanio, color):
        super().__init__(pos_inicial, tamanio, 0, color)
        self.visible = True

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
            
            if enemigo.rectangulo.right > pantalla.get_height() or enemigo.rectangulo.left < 10:
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
    
def crear_colmena(colmena: list) -> int:
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
            elif index_fila == 2 or index_fila == 3:
                puntaje = 20
            else:
                puntaje = 10
            enemigo = Enemigo((enemy_pos_x,enemy_pos_y),(30,30),15,"Green",puntaje)
            enemy_pos_y = enemy_pos_y + 60
            columna_enemigos.append(enemigo)
            cantidad_enemigos = cantidad_enemigos +1
        colmena.append(columna_enemigos)

        enemy_pos_x = enemy_pos_x + 60
    
    return cantidad_enemigos
    
#Funciones barreras
def crear_barrera(pos_x,pos_y,barrera):
    barrera_pos_x = pos_x
    for columna in range(4):
        barrera_pos_y = pos_y
        columna_barrera = []
        for elemento in range(4):
            elemento = Barrera((barrera_pos_x,barrera_pos_y),(30,30),"Blue")
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

#start
def nivel_1():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    RELOJ = pygame.time.Clock()
    FPS = 60

    ANCHO = 750
    ALTO = 900

    pantalla = pygame.display.set_mode((ANCHO,ALTO))

    game_manager = GameManager(True,0,3,0)
    sound_manager = SoundManager(pygame.mixer.Sound("sounds\\DisparoJugador.wav"),pygame.mixer.Sound("sounds\\DisparoEnemigo.wav"),pygame.mixer.Sound("sounds\\ExplosionJugador.wav"),pygame.mixer.Sound("sounds\\ExplosionEnemigo.wav"),[pygame.mixer.Sound("sounds\\Paso1.wav"),pygame.mixer.Sound("sounds\\Paso2.wav"),pygame.mixer.Sound("sounds\\Paso3.wav"),pygame.mixer.Sound("sounds\\Paso4.wav")])

    jugador = Jugador((ANCHO/2,ALTO-30),(30,30),5,"White", pygame.K_LEFT, pygame.K_RIGHT,game_manager.vidas_jugador)
    proyectil_jugador = Proyectil((-100,-100),(5,30),0,"White", False)

    listado_barreras = []

    fortaleza_pos_x = 50

    crear_fortaleza(fortaleza_pos_x,listado_barreras)

    matriz_enemigos = []
    disparos_enemigos = []

    game_manager.cantidad_enemigos = crear_colmena(matriz_enemigos)

    #update
    while True:
        RELOJ.tick(FPS)
        delta_time = RELOJ.tick(FPS) / 1000

        teclas_presionadas = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pantalla.fill("Black")
        game_manager.update()
        pantalla.blit(game_manager.text_puntaje, (10, 10))

        if not jugador.con_vida or game_manager.cantidad_enemigos <= 0:
            game_manager.juego_activo = False

            
        if game_manager.juego_activo:
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
            if not jugador.con_vida:
                if game_manager.vidas_jugador > 1:  
                    pantalla.blit(game_manager.mensaje_vida_perdida,(ANCHO/2,ALTO/2))
                    game_manager.vidas_jugador = game_manager.vidas_jugador - 1
                    jugador.con_vida = True
                    game_manager.juego_activo = True
                    pygame.display.flip()
                    pygame.time.delay(3000)
                else:
                    pantalla.blit(game_manager.mensaje_game_over,(ANCHO/2,ALTO/2))
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    pygame.quit()
                    sys.exit()
            elif game_manager.cantidad_enemigos <= 0:
                pantalla.blit(game_manager.mensaje_ganaste,(ANCHO/2,ALTO/2))
                pygame.time.delay(3000)
                pygame.quit()
                sys.exit()


nivel_1()