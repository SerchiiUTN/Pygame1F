import pygame

def reescalar_imagen(lista_imagenes, tamanio):
    for i in range(len(lista_imagenes)):
        lista_imagenes[i] = pygame.transform.scale(lista_imagenes[i],tamanio)


personaje_sprite = [pygame.image.load("sprites/Nave_UTN.png"),
                    pygame.image.load("sprites/Nave_explota.png")]

enemigo_sprite = [pygame.image.load("sprites/alien10.png"),
                  pygame.image.load("sprites/alien20.png"),
                  pygame.image.load("sprites/alien30.png")]

titulo_sprite = [pygame.image.load("sprites/title_space_invaders.png")]