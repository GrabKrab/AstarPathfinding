import os

import pygame
from Game.constants.constants import *
from Game.mapa import Mapa
from Game.patchfinding import Pathfinding
from Game.mouse import *
from Game.jednostki import Unit

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 30)

pygame.init()
font = pygame.font.SysFont("arial", 15, True)
global mainWindow, mapa
mainWindow = pygame.display.set_mode((wholeScreen_width, wholeScreen_height))

bg = pygame.image.load(bg_file_path)    # load backgroung file
mainWindow.blit(bg, (0, 0))             # put it on screen

pygame.display.set_caption("Warlords")

map_filename = r'D:\Projects\Python\WarlordsGame\Game\maps\erythea.txt'
mapa = Mapa(map_filename, mapImages, mapLegenda, mainWindow)

current_unit = Unit("Scout", [0, 0])

#################################
# for y in range(10, 10):
#     zipok = []
#     for x in range(mapa.mapaWid):
#         zipok.append(zmienna[y][x])
#     print(zipok)
#     pipi.append(zipok)

pygame.display.update()


def get_distance(node_start, node_end):
    """Node_start i node_end = tuple(x,y)
    Node_start = starting point on map
    Node_end = ending point on map

    Calculates the distance between starting and ending node.
    Every horiz/vertic move i distances cost of 10
    Every diagonal move is a distance of 14 (pitagoras)
    """
    # horizontal distance between two nodes
    x1, x2 = node_start[0], node_end[0]
    y1, y2 = node_start[1], node_end[1]

    x = abs(x1 - x2)
    y = abs(y1 - y2)

    print("x, y ", x, y)

    if x > y:
        print("diagonal moves ", y)
        print("Hor/Vert moves ", x-y)
        return 14 * y + 10 * (x - y)
    else:
        print("diagonal moves ", x)
        print("Hor/Vert moves ", y-x)
        return 14 * x + 10 * (y - x)


def rysuj_nody_new(start, end):
    for y in range(tiles_y):  # rysowanie nodow na mapie
        for x in range(tiles_x):
            Gcost = get_distance(start, (x + mapOffset[0], y + mapOffset[1]))
            Hcost = get_distance(end, (x + mapOffset[0], y + mapOffset[1]))
            Fcost = Gcost + Hcost
            Tcost = mapa.cost[y + mapOffset[1]][x + mapOffset[0]]
            if Tcost < 1:
                total_cost = " "
            else:
                total_cost = (Tcost * 10 + Fcost)
            text = font.render(str(Fcost), 1, (0, 0, 0))
            mainWindow.blit(text, (x * tile_dim + tile_dim, y * tile_dim + tile_dim))




def rysuj_nody(nods):
    for y in range(tiles_y):  # rysowanie nodow na mapie
        for x in range(tiles_x):
            stry = str(nods[y + mapOffset[1]][x + mapOffset[0]])
            text = font.render(stry, 1, (0, 0, 0))
            mainWindow.blit(text, (x * tile_dim + tile_dim - 8, y * tile_dim + tile_dim - 8))


def rysuj_nody_cel(nods_end, nods_start):
    for y in range(tiles_y):  # rysowanie nodow na mapie
        for x in range(tiles_x):
            stry1 = int(nods_end[y + mapOffset[1]][x + mapOffset[0]])
            text = font.render(str(stry1), 1, (0, 0, 0))
            mainWindow.blit(text, (x * tile_dim + tile_dim-8, y * tile_dim + tile_dim-8))
            stry2 = int(nods_start[y + mapOffset[1]][x + mapOffset[0]])
            text = font.render(str(stry2+stry1), 1, (0, 0, 0))
            # mainWindow.blit(text, (x * tile_dim + tile_dim+22, y * tile_dim + tile_dim+12))
            stry3 = int(mapa.cost[y + mapOffset[1]][x + mapOffset[0]])
            stry_sum = str(stry1 + stry2 + stry3)

            text = font.render(stry_sum, 1, (0, 0, 0))
            mainWindow.blit(text, (x * tile_dim + tile_dim+5, y * tile_dim + tile_dim+5))
            # koszty = str(mapa.cost[y + mapOffset[1]][x + mapOffset[0]])
            # textcost = font.render(koszty, 1, (0, 0, 0))
            # mainWindow.blit(text, (x * tile_dim + tile_dim, y * tile_dim + tile_dim))


def land_status(node):
    terrain = mapa.mapa[node[1]][node[0]]
    if terrain < 20:
        return "sea"
    else:
        return "land"


run = True
mapa.rysuj_mape(mapOffset[0], mapOffset[1])
while run:
    for event in pygame.event.get():    # sprawdza możliwość wyjścia z programu
        if event.type == pygame.QUIT:
            run = False

    # check for mouse
    # pygame.event.get()
    mouse = pygame.mouse.get_pressed()
    x, y, where = mouse_coords(mapa)

    if mouse == (True, False, False):

        print("Start node XY: ", x + mapOffset[0], y + mapOffset[1])
        print(where)
        print("offset ", mapOffset)
        if where == "on_map_move":
            mapOffset = move_offset(x, y)
            mapa.rysuj_mape(mapOffset[0], mapOffset[1])
            pygame.display.update()
        elif where == "on_mini":
            mapOffset = move_offset_mini(x, y)
            mapa.rysuj_mape(mapOffset[0], mapOffset[1])
            pygame.display.update()
            print("mini")
        elif where == "on_map":
            start_node = (x + mapOffset[0], y + mapOffset[1])
            current_unit.land_status = land_status(start_node)
        else:
            pass
        pygame.time.wait(1000)

    if mouse == (False, False, True):
        if where == "on_map":
            end_node = (x + mapOffset[0], y + mapOffset[1])
            print(current_unit.land_status)

            # path = Pathfinding(start_node, end_node, mapa, mainWindow, unit=current_unit)
            current_unit.path = Pathfinding(start_node, end_node, mapa, mainWindow)
            print(f'{current_unit.name} path length', current_unit.path.length)
            # path.find_path(start_node, end_node, mapa, mainWindow)
            # a = path.path

            # pygame.draw.rect(mainWindow, GREEN, [x * tile_dim, y * tile_dim, 20, 20])

            pygame.display.update()
            # rysuj_nody_new(start_node, end_node)
            # nodcos_cel = path.make_nodes(x + mapOffset[0], y + mapOffset[1])
            # rysuj_nody_cel(nodcos_cel, nodcos)

        # if where == "on_map" and len(nodcos) > 0:
        #     pass
            # a = path.make_path(x + mapOffset[0], y + mapOffset[1], nodcos)
            # print('path', a)

    pygame.display.update()
    # if mouse == (False, False, True):   # prawy klawisz -> pkt koncowy
    #     dest_p = destination_point()
    #     print("dest point ", dest_p)
    #     if dest_p:
    #         path = znajdz_path(dest_p[0], dest_p[1], dest_p[2])  # [0] - dest_x, [1] - dest_y, [2] - lista nodow
    #         print("path", path)
    #         # rysuj_mape()
    #         narysuj_scieżkę(path)
    #         pygame.display.update()

pygame.quit()