from Game.constants.constants import unit_image
from pygame import transform


class Unit(object):
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.tile_dim = 40
        self.image = transform.scale(unit_image, (self.tile_dim-1, self.tile_dim-1))
        self.land_status = "land"  # /"sea" /"air" default is "land"
        self.path = []
#       na poczatek klikniecie lewej myszy bedzie okreslało parametr 'where'
