from Game.constants.constants import *
from pygame import mouse, cursors
import pygame


def mouse_coords(mapa):
    where = ("on_map_move", "on_map", "on_mini", "on_buttons", "on_panel")
    cursor = ()  # tu bedzie zapisany jaki kursor na jakim obsszarze mapy

    mouse_pos = mouse.get_pos()  # absolutne wartości myszy

    # czy jest w obrębie mapy, jeśli tak zwraca współrzędne mapy i opis "on_map"
    mouseX = (mouse_pos[0] - mapstartpoint) // tile_dim    # MuouseX a nie X, b jezeli mapa bedzie zoffsetowana (to X = mouseX + Offset)
    mouseY = (mouse_pos[1] - mapstartpoint) // tile_dim    # j.w.
    if 0 <= mouseX <= tiles_x - 1 and 0 <= mouseY <= tiles_y - 1:  # czy jest w obrebie mapy
        if mouseX < 1 or mouseX > tiles_x - 2 or mouseY < 1 or mouseY > tiles_y - 2:  # czy jest na brzegowych kratkach

            a, b, c, d = pygame.cursors.tri_left
            pygame.mouse.set_cursor(a, b, c, d)

            return mouseX, mouseY, where[0]
        else:

            a, b, c, d = pygame.cursors.arrow
            pygame.mouse.set_cursor(a, b, c, d)

            return mouseX, mouseY, where[1]

    elif miniMapXY[0] < mouse_pos[0] < miniMapXY[0] + mapaWid * rd \
         and miniMapXY[1] < mouse_pos[1] < miniMapXY[1] + mapaHgh * rd:

        a, b, c, d = pygame.cursors.diamond
        pygame.mouse.set_cursor(a, b, c, d)

        return mouse_pos[0], mouse_pos[1], where[2]
    else:

        a, b, c, d = pygame.cursors.broken_x
        pygame.mouse.set_cursor(a, b, c, d)

        return mouse_pos[0], mouse_pos[1], where[4]


def move_offset(x, y):
    if x == 0 and mapOffset[0] > 0:
        mapOffset[0] -= 1
    if x == tiles_x - 1 and mapOffset[0] < mapaWid - tiles_x:
        mapOffset[0] += 1
    if y == 0 and mapOffset[1] > 0:
        mapOffset[1] -= 1
    if y == tiles_y - 1 and mapOffset[1] < mapaHgh - tiles_y:
        mapOffset[1] += 1
    return mapOffset


def move_offset_mini(mX, mY):
    if mX < miniMapXY[0] + (tiles_x * rd) // 2:
        mapOffset[0] = 0
    elif mX > miniMapXY[0] + (mapaWid * rd) - (tiles_x * rd // 2):
        mapOffset[0] = mapaWid - tiles_x
    else:
        mapOffset[0] = (mX - miniMapXY[0]) // rd - tiles_x // 2
    if mY < miniMapXY[1] + (tiles_y * rd) // 2:
        mapOffset[1] = 0
    elif mY > miniMapXY[1] + (mapaHgh * rd) - (tiles_y * rd // 2):
        mapOffset[1] = mapaHgh - tiles_y
    else:
        mapOffset[1] = (mY - miniMapXY[1]) // rd - tiles_y // 2
    return mapOffset
