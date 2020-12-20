from pygame import image, font, display

# terr, kolor on mimimap, koszt
mapLegenda = {0: [0, (42, 186, 220), 0],  # [0] water , [1] kolor Blue, [2] koszt_przejazdu
              1: [1, (42, 186, 255), 0],  # brzeg
              2: [2, (42, 186, 255), 0],  # brzeg
              3: [3, (42, 186, 255), 0],  # brzeg
              4: [4, (42, 186, 255), 0],  # brzeg
              5: [5, (42, 186, 255), 0],  # brzeg
              6: [6, (42, 186, 255), 0],  # brzeg
              7: [7, (42, 186, 255), 0],  # brzeg
              8: [8, (42, 186, 255), 0],  # brzeg
              9: [9, (42, 186, 255), 0],  # brzeg
              10: [10, (42, 186, 255), 0],  # brzeg
              11: [11, (42, 186, 255), 0],  # brzeg
              12: [12, (42, 186, 255), 0],  # brzeg
              13: [13, (42, 186, 255), 0],  # brzeg
              14: [14, (42, 186, 255), 0],  # brzeg
              15: [15, (42, 186, 255), 0],  # brzeg
              16: [16, (42, 186, 255), 0],  # brzeg
              20: [17, (81, 140, 28), 2],  # [0] plain , [1] kolor green
              21: [18, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              22: [19, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              23: [20, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              24: [21, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              25: [22, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              26: [23, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              27: [24, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              28: [25, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              29: [26, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              30: [27, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              31: [28, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              32: [29, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              33: [30, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              34: [31, (150, 75, 0), 1],  # [0] droga , [1] kolor brąz
              35: [32, (150, 75, 0), 1],  # [0] most , [1] kolor brąz
              36: [33, (150, 75, 0), 1],  # [0] most , [1] kolor brąz
              37: [34, (150, 75, 0), 1],  # [0] most , [1] kolor brąz
              38: [35, (150, 75, 0), 1],  # [0] most , [1] kolor brąz
              40: [36, (0, 102, 0), 3],  # [0] las , [1] ciemno zielony
              41: [37, (0, 102, 0), 3],
              42: [38, (0, 75, 0), 3],
              43: [39, (0, 75, 0), 3],
              44: [40, (0, 75, 0), 3],
              45: [41, (0, 75, 0), 3],
              46: [42, (0, 75, 0), 3],
              47: [43, (0, 75, 0), 3],
              49: [44, (70, 70, 200), 4],   # bagno # jasno nieb
              50: [45, (50, 130, 50), 5],     # wzgórza szara zieleń
              51: [46, (50, 130, 50), 5],
              52: [47, (50, 130, 50), 5],
              53: [48, (50, 130, 50), 5],
              54: [49, (128, 128, 128), -2],     # góry szay
              55: [50, (128, 128, 128), -2],     # góry szay
              56: [51, (128, 128, 128), -2],     # góry szay
              57: [52, (128, 128, 128), -2],     # góry szay
              58: [53, (128, 128, 128), -2],     # góry szay
              59: [54, (128, 128, 128), -2],     # góry szay
              60: [55, (0, 0, 0), 1],     # miasto
              61: [56, (0, 0, 0), 1],     # miasto
              62: [57, (0, 0, 0), 1],     # miasto
              63: [58, (0, 0, 0), 1],     # miasto
              64: [59, (255, 255, 255), 1],     # ruiny
              65: [60, (255, 255, 255), 1],     # swiatynia 1
              66: [61, (255, 255, 255), 1],     # swiatynia 2
              }

# Tile images:
img_dir = "D:/Projects/Python/Pygame/Warlords/map_img/"
mapImages = [image.load(img_dir + 'water.jpg'),
             image.load(img_dir + 'b1.jpg'),
             image.load(img_dir + 'b2.jpg'),
             image.load(img_dir + 'b3.jpg'),
             image.load(img_dir + 'b4.jpg'),
             image.load(img_dir + 'b5.jpg'),
             image.load(img_dir + 'b6.jpg'),
             image.load(img_dir + 'b7.jpg'),
             image.load(img_dir + 'b8.jpg'),
             image.load(img_dir + 'b9.jpg'),
             image.load(img_dir + 'b10.jpg'),
             image.load(img_dir + 'b11.jpg'),
             image.load(img_dir + 'b12.jpg'),
             image.load(img_dir + 'b13.jpg'),
             image.load(img_dir + 'b14.jpg'),
             image.load(img_dir + 'b15.jpg'),
             image.load(img_dir + 'b16.jpg'),
             image.load(img_dir + 'plain.jpg'),    # równina
             image.load(img_dir + 'd1.jpg'),       # drogi
             image.load(img_dir + 'd2.jpg'),
             image.load(img_dir + 'd3.jpg'),
             image.load(img_dir + 'd4.jpg'),
             image.load(img_dir + 'd5.jpg'),
             image.load(img_dir + 'd6.jpg'),
             image.load(img_dir + 'd7.jpg'),
             image.load(img_dir + 'd8.jpg'),
             image.load(img_dir + 'd9.jpg'),
             image.load(img_dir + 'd10.jpg'),
             image.load(img_dir + 'd11.jpg'),
             image.load(img_dir + 'd12.jpg'),
             image.load(img_dir + 'd13.jpg'),
             image.load(img_dir + 'd14.jpg'),
             image.load(img_dir + 'm1.jpg'),       # mosty
             image.load(img_dir + 'm2.jpg'),
             image.load(img_dir + 'm3.jpg'),
             image.load(img_dir + 'm4.jpg'),
             image.load(img_dir + 'l.jpg'),        # lasy
             image.load(img_dir + 'l1.jpg'),
             image.load(img_dir + 'l2.jpg'),
             image.load(img_dir + 'l3.jpg'),
             image.load(img_dir + 'l4.jpg'),
             image.load(img_dir + 'l5.jpg'),
             image.load(img_dir + 'l6.jpg'),
             image.load(img_dir + 'l7.jpg'),
             image.load(img_dir + 'bg.jpg'),       # bagno
             image.load(img_dir + 'w1.jpg'),       # wzgórza
             image.load(img_dir + 'w2.jpg'),
             image.load(img_dir + 'w3.jpg'),
             image.load(img_dir + 'w3.jpg'),
             image.load(img_dir + 'g1.jpg'),       # góry
             image.load(img_dir + 'g2.jpg'),
             image.load(img_dir + 'g3.jpg'),
             image.load(img_dir + 'g4.jpg'),
             image.load(img_dir + 'g5.jpg'),
             image.load(img_dir + 'g6.jpg'),
             image.load(img_dir + 'c1.jpg'),       # miasta
             image.load(img_dir + 'c2.jpg'),
             image.load(img_dir + 'c3.jpg'),
             image.load(img_dir + 'c4.jpg'),
             image.load(img_dir + 'ruin.jpg'),       # ruiny
             image.load(img_dir + 'sw1.jpg'),       # swiatynia 1
             image.load(img_dir + 'sw2.jpg'),       # swiatynia 2
             ]

# font_nod = font.SysFont("arial", 20, True)
# fullScreenModes = display.list_modes()  # print(fullScreenModes)
wholeScreen_width = 1242
wholeScreen_height = 790
map_width = 800         # szerokość Mapy w pixelach
map_height = 600        # wysokość Mapy w pixelach
mapaWid = 110
mapaHgh = 150
mapstartpoint = 32
mapOffset = [0, 0]      # początkowy offset dla Mapy X, Y
miniMapXY = (881, 32)   # polożenie miniMapy
rd = 3
tile_dim = 40
tiles_x = map_width // tile_dim      # ilość kratek na całym ekranie w osi x
tiles_y = map_height // tile_dim     # w osi y

map_file_path = "D:\Projects\Python\WarlordsGame\Game\img\map_img"
bg_file_path = "D:\Projects\Python\WarlordsGame\Game\img\WarlordsHUD2.jpg"


wymiary_okna_mapy = 653, (352, 348), (25, 21)
wymiary_okna_mini = (407, 565), (921, 304), (717, 21)


# COLORS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# UNITS

units_dir = "D:/Projects/Python/WarlordsGame/Game/img/units/"

unit_image = image.load(units_dir + 'scout.jpg')  # pojedynczy na teraz, potem bedzie wiecej

# unit_images = [image.load(units_dir + 'scout.jpg')] # to bedzie pełna lista jednostek
