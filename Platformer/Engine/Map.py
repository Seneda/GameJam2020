import os

import pygame

MAPS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Resources", "maps")
TILES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Resources", "tiles")

def LoadTileMap(map_filename, tile_dict):
    tiles = []
    with open(os.path.join(MAPS_DIR, map_filename)) as f:
        mapdef = [[i for i in line.strip()] for line in f.readlines()]
    for y in range(0, len(mapdef)):
        row = mapdef[y]
        tiles.append([])
        for x in range(0, len(row)):
            tiles[y].append(tile_dict.get(mapdef[y][x], None))
    return tiles

tile_dict = {
           "0": None,
           "1": pygame.image.load(os.path.join(TILES_DIR, "groundtop.png")),
           "2": pygame.image.load(os.path.join(TILES_DIR, "wall.png")),
           "3": pygame.image.load(os.path.join(TILES_DIR, "ground.png"))
           }

