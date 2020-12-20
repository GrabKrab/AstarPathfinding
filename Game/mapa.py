import pygame
from pygame import transform
from Game.constants.constants import mapOffset


class Mapa(object):

    def __init__(self, mapa, m_images, mapLegend, todraw):

        self.mapa = self.load_map(mapa)                     # lista z wartościami 'tile'
        self.mapaWid = len(self.mapa[0])                    # szer mapy wg pliku
        self.mapaHgh = len(self.mapa)                       # wys mpy wg pliku
        self.mapLegend = mapLegend
        self.cost = self.costs(legenda=self.mapLegend)           # kopia 'mapa' lecz z wartosciami 'cost'
        self.tile_dim = 40                                  # wymiary pojedyńczej lokacji (kratki) na mapie w pixelach
        self.images = self.zoom_img(m_images)               # list of images of 'tiles'
        self.map_width = 800                                # szerokość Mapy w pixelach
        self.map_height = 600                               # wysokość Mapy w pixelach
        self.mapstartpoint = 32
        self.tiles_x = self.map_width // self.tile_dim      # ilość kratek na całym ekranie w osi x
        self.tiles_y = self.map_height // self.tile_dim     # w osi y
        self.mapOffset = [0, 0]                             # początkowy offset dla Mapy
        self.miniMapXY = (881, 32)                          # polożenie miniMapy
        self.rd = 3                                         # pojedyńczy tile na minimapie
        self.window = todraw

    def costs(self, legenda):
        costs = []
        for y in range(self.mapaHgh):
            line = []
            for x in range(self.mapaWid):
                line.append(legenda.get(self.mapa[y][x])[2])
            costs.append(line)
        return costs

    def zoom_img(self, map_im):
        # Zoom obrazków mapy do wielkości tile_dim
        map_img = []
        for image in map_im:
            map_img.append(pygame.transform.scale(image, (self.tile_dim-1, self.tile_dim-1)))
        return map_img

    def load_map(self, filename):
        with open(filename, 'r') as mapaFile:
            extract_file = mapaFile.read().splitlines()
            map_lines = []
            for line in extract_file:
                line.split(",")
                map_lines.append(line)

            mapa = []
            # c=1
            for line in map_lines:
                map_row = []
                map_rowstr = line[:-1].split(",")
                for l in map_rowstr:
                    map_row.append(int(l))
                mapa.append(map_row)
            # for i in mapa:  # jakbym podupczył w pliku, to ta petla mi sprawdzi długości
            #     print("linia nr {}, len = {}".format(c,len(i)))
            #     c+=1
        return mapa

    def rysuj_mape(self, offx, offy):  # rysuje mape głowna
        self.mapOffset = [offx, offy]
        for y in range(self.tiles_y):
            for x in range(self.tiles_x):
                tilePic = self.mapLegend.get(self.mapa[y + offy][x + offx])
                self.window.blit(self.images[tilePic[0]], (x * self.tile_dim + self.mapstartpoint,
                                                           y * self.tile_dim + self.mapstartpoint))

        self.rysuj_mini_mape()

    def rysuj_mini_mape(self):  # rysuje minimape
        for y in range(self.mapaHgh):
            for x in range(self.mapaWid):
                tileCol = self.mapLegend.get(self.mapa[y][x])  # pobiera wartości koloru dla dla rodzaju terenu z dict
                pygame.draw.rect(self.window, (tileCol[1]),
                                 pygame.Rect(self.miniMapXY[0] + x * self.rd,
                                             self.miniMapXY[1] + y * self.rd, self.rd, self.rd))

                ramMinMapySr = (self.tiles_x // 2, self.tiles_y // 2)
                pygame.draw.rect(self.window, (255, 255, 255),
                                 pygame.Rect(self.miniMapXY[0] + self.mapOffset[0] * self.rd,
                                             self.miniMapXY[1] + self.mapOffset[1] * self.rd,
                                             self.tiles_x * self.rd, self.tiles_y * self.rd), 1)

    def get_world_pos(self, x, y):
        return x + mapOffset[0], y + mapOffset[1]


# mL2Dk = []                      # lista zawierające wartości (nr. rysunków) z mapLegenda2
# for key in mapLegenda.keys():  # potrzebna do przewijania kafelkow lewo prawo w progr. tworzenie mapy
#     mL2Dk.append(key)

