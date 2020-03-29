import os
import sys

import pygame
import pygame.locals

MAPS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Resources", "maps")
TILES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Resources", "tiles")
BG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Resources", "background")


class Map(object):
    def __init__(self, tilemap_file):
        self.parse_tilemap_file(tilemap_file+'.txt')

    def parse_tilemap_file(self, tilemap_file):
        with open(os.path.join(MAPS_DIR, tilemap_file)) as f:
            data = f.read()
        sections = [l.split() for l in data.strip().split('# ')]
        sections = {k[0]: k[1:] for k in sections if len(k) > 1}
        self.tileset = {}
        for i in range(0, len(sections['Tileset']), 2):
            print(i)
            try:
                self.tileset[sections["Tileset"][i]] = pygame.image.load(
                    os.path.join(TILES_DIR, sections["Tileset"][i + 1]))
            except Exception as e:
                print("Error: Could not load tileset")
                print(e)
        tilelayout = [[i for i in line.strip()] for line in sections['Tilelayout']]
        self.tiles = []
        for y in range(0, len(tilelayout)):
            row = tilelayout[y]
            self.tiles.append([])
            for x in range(0, len(row)):
                self.tiles[y].append(self.tileset.get(tilelayout[y][x], None))
        backgrounds = sections['Backgrounds']
        self.background_layers = []
        for i in range(0, len(backgrounds), 3):
            image_file, parallax_x, parallax_y = backgrounds[i:i+3]
            print(image_file)
            self.background_layers.append((pygame.image.load(os.path.join(BG_DIR, image_file)), (int(parallax_x), int(parallax_y))))

    @property
    def size(self):
        return (16*len(self.tiles[0]), 16*len(self.tiles))

    def draw(self, display, minimap=None, scroll=(0, 0)):
        for i, (bgimage, parallax) in enumerate(self.background_layers):
            offsets = [-1, 0, 1]
            scroll_offset = round(abs(scroll[0]/parallax[0]+display.get_width()/2)/display.get_width())
            for offset in offsets:
                if i == 0:
                    bgrect = pygame.Rect(*((offset+scroll_offset)*display.get_width() - scroll[0]/parallax[0], 0 - scroll[1]/parallax[1]), *(display.get_width(), display.get_height()))
                    minimap.blit(pygame.font.SysFont('Arial', 50).render('BG:{:d}'.format(offset), True, (0, 0, 0)), (bgrect.centerx, bgrect.centery+50))
                display.blit(pygame.transform.scale(bgimage, (display.get_width(), display.get_height())), ((offset+scroll_offset)*display.get_width() - scroll[0]/parallax[0], 0 - scroll[1]/parallax[1]))

        rects = []
        for y in range(0, len(self.tiles)):
            for x in range(0, len(self.tiles[y])):
                tile = self.tiles[y][x]
                if tile is not None:
                    display.blit(tile, (x * 16 - scroll[0], y * 16 - scroll[1], 16, 16))
                    rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                    if minimap:
                        pygame.draw.rect(minimap, (255, 0, 255), rects[-1])
        if minimap:
            pygame.draw.rect(minimap, (255, 255, 0), pygame.Rect(*scroll, display.get_width(), display.get_height()), 4)
        return rects


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

if __name__ == "__main__":
    map = Map("test_map_new_format.txt", "")
    pygame.init()
    WINDOW_SIZE = (int(1920*0.75), int(1080*0.75))
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
    display = pygame.Surface(map.size)
    map.draw(display)
    screen.blit(display, (0, 0))
    pygame.display.update()

    while True:
        for event in pygame.event.get():  # event loop
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
