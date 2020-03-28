import os
import sys
from random import random

import pygame
import pygame.locals

from Character import Character

pygame.init()
WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
display = pygame.Surface((300, 200))
clock = pygame.time.Clock()

key_state = {"Up": False, "Down": False, "Left": False, "Right": False}

background_color = (100, 100, 100)
time = 0
sprite_pos = [50, 50]


def ProcessPygameEvents(key_state):
    for event in pygame.event.get():  # event loop
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_UP:
                key_state["Up"] = True
            if event.key == pygame.locals.K_DOWN:
                key_state["Down"] = True
            if event.key == pygame.locals.K_LEFT:
                key_state["Left"] = True
            if event.key == pygame.locals.K_RIGHT:
                key_state["Right"] = True
        if event.type == pygame.locals.KEYUP:
            if event.key == pygame.locals.K_UP:
                key_state["Up"] = False
            if event.key == pygame.locals.K_DOWN:
                key_state["Down"] = False
            if event.key == pygame.locals.K_LEFT:
                key_state["Left"] = False
            if event.key == pygame.locals.K_RIGHT:
                key_state["Right"] = False
    return key_state


# def UpdatePosition(sprite_pos):
#     speed = 1
#     if key_state['Right']:
#         sprite_pos[0] += speed
#     if key_state['Left']:
#         sprite_pos[0] -= speed
#     if key_state['Down']:
#         sprite_pos[1] += speed
#     if key_state['Up']:
#         sprite_pos[1] -= speed
#     return sprite_pos

def UpdateBackgroundColour(background_color):
    r, g, b = background_color
    r += random() * 1 * (random() > 0.5)
    g += random() * 1 * (random() > 0.5)
    b += random() * 1 * (random() > 0.5)
    r = max(50, r)
    g = max(50, g)
    b = max(50, b)
    r %= 255
    g %= 255
    b %= 255
    return (r, g, b)


MAPS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Resources", "maps")
TILES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Resources", "tiles")

tile_dict = {
           "0": None,
           "1": pygame.image.load(os.path.join(TILES_DIR, "groundtop.png")),
           "2": pygame.image.load(os.path.join(TILES_DIR, "wall.png")),
           "3": pygame.image.load(os.path.join(TILES_DIR, "ground.png"))
           }

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

Map = LoadTileMap("test_map.txt", tile_dict)

Finley = Character(screen, 'Finley', [50, 100])
Scuttle = Character(screen, 'Scuttlefish', [70, 100])

# Loading in floor
# floor = pygame.Rect(300,10,100,100)

def DrawMap(display, tilemap):
    rects = []
    for y in range(0, len(tilemap)):
        for x in range(0, len(tilemap[y])):
            tile = tilemap[y][x]
            if tile is not None:
                display.blit(tile, (x*16, y*16, 16, 16))
                rects.append(pygame.Rect(x*16, y*16, 16, 16))
    return rects

while True:  # game loop
    time += 1
    key_state = ProcessPygameEvents(key_state)
    display.fill(background_color)  # clear screen by filling it with blue

    map_rects = DrawMap(display, Map)
    # sprite_pos = UpdatePosition(sprite_pos)
    Finley.updatePos(key_state, 1, map_rects)
    Scuttle.updatePos(key_state, 1, map_rects)

    background_color = UpdateBackgroundColour(background_color)


    # display.blit(sprites['Finley']['walk'][int(time / 10) % len(sprites['Finley']['walk'].keys())], sprite_pos)


    Finley.updateDraw(display)
    Scuttle.updateDraw(display)


    # display.blit(animation[int(time / 10) % len(animation.keys())], Finley.pos)

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))

    pygame.display.update()
    clock.tick(60)
