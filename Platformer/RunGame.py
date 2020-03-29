import os
import sys
from random import random
import time

import pygame
import pygame.locals
import pygame.sprite

from Engine.Character import Character
from Engine.Map import LoadTileMap, tile_dict

pygame.init()
WINDOW_SIZE = (1200, 800)
WINDOW_PIXELS = (300, 200)

Map = LoadTileMap("test_map.txt", tile_dict)

MAP_SIZE = (16*len(Map[0]), 16*len(Map))

BG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Resources", "background")


screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
display = pygame.Surface(WINDOW_PIXELS)
minimap = pygame.Surface(MAP_SIZE)
clock = pygame.time.Clock()

# key_state = {"Up": False, "Down": False, "Left": False, "Right": False}

background_color = (100, 100, 100)
sprite_pos = [50, 50]

class KeyState:
  def __init__(self):
    self.up = False
    self.down = False
    self.left = False
    self.right = False

# Controller 0 is Arrow
# Controller 1 is WASD
def ProcessPygameEvents(controllers,key_states):
    controllerKeys = [[pygame.locals.K_UP,pygame.locals.K_DOWN,pygame.locals.K_LEFT,pygame.locals.K_RIGHT],\
                [pygame.locals.K_w,pygame.locals.K_s,pygame.locals.K_a,pygame.locals.K_d]]

    for event in pygame.event.get():  # event loop
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
        for controller in controllers: 
            if event.type == pygame.locals.KEYDOWN:
                if event.key == controllerKeys[controller][0]:
                    key_states[controller].up = True
                if event.key == controllerKeys[controller][1]:
                    key_states[controller].down = True
                if event.key == controllerKeys[controller][2]:
                    key_states[controller].left = True
                if event.key == controllerKeys[controller][3]:
                    key_states[controller].right = True
            if event.type == pygame.locals.KEYUP:
                if event.key == controllerKeys[controller][0]:
                    key_states[controller].up = False
                if event.key == controllerKeys[controller][1]:
                    key_states[controller].down = False
                if event.key == controllerKeys[controller][2]:
                    key_states[controller].left = False
                if event.key == controllerKeys[controller][3]:
                    key_states[controller].right = False

    return key_states


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


Treeman = Character(screen, 'Treeman', [20, 80])
Scuttle = Character(screen, 'Scuttlefish', [70, 100])

# Loading in floor
# floor = pygame.Rect(300,10,100,100)

def DrawMap(display, minimap, tilemap, scroll):
    rects = []
    for y in range(0, len(tilemap)):
        for x in range(0, len(tilemap[y])):
            tile = tilemap[y][x]
            if tile is not None:
                display.blit(tile, (x*16-scroll[0], y*16-scroll[1], 16, 16))
                rects.append(pygame.Rect(x*16, y*16, 16, 16))
                pygame.draw.rect(minimap, (255, 0, 0), rects[-1], 1)
    pygame.draw.rect(minimap, (255, 255, 0), pygame.Rect(*scroll, *WINDOW_PIXELS), 2)

    return rects

scroll = [0, 0]

scroll[0] = Treeman.x - WINDOW_PIXELS[0] / 2
scroll[1] = Treeman.y - 2 * WINDOW_PIXELS[1] / 3

bgimage = pygame.image.load(os.path.join(BG_DIR, 'parallax_mountain_pack', 'layers', 'parallax-mountain-bg.png'))
mgimage = pygame.image.load(os.path.join(BG_DIR, 'parallax_mountain_pack', 'layers', 'parallax-mountain-mountain-far.png'))
fgimage = pygame.image.load(os.path.join(BG_DIR, 'parallax_mountain_pack', 'layers', 'parallax-mountain-foreground-trees.png'))
t0 = time.time()

arrow_key_state = KeyState()
wasd_key_state = KeyState()
controllers = [0,1]
key_states =[arrow_key_state,wasd_key_state]

while True:  # game loop
    t_step = time.time()

    key_states = ProcessPygameEvents(controllers,key_states)
    arrow_key_state = key_states[0]
    wasd_key_state = key_states[1]

    # background_color = UpdateBackgroundColour(background_color)
    display.fill(background_color)
    display.blit(pygame.transform.scale(bgimage, WINDOW_PIXELS), (0, 0))
    for i in [-2, -1, 0, 1, 2]:
        display.blit(pygame.transform.scale(mgimage, WINDOW_PIXELS), (i*WINDOW_PIXELS[0]-scroll[0]/10, 0-scroll[1]/10))
    for i in [-2, -1, 0, 1, 2]:
        display.blit(pygame.transform.scale(fgimage, WINDOW_PIXELS), (i*WINDOW_PIXELS[0]-scroll[0]/3, 0-scroll[1]/2))
    minimap.fill([255, 0, 255])
    minimap.set_colorkey((255, 0, 255))

    scroll[0] = scroll[0] + ((Treeman.x - WINDOW_PIXELS[0] / 2) - scroll[0])/5
    scroll[1] = scroll[1] + ((Treeman.y - 2 * WINDOW_PIXELS[1] / 3) - scroll[1])/10


    map_rects = DrawMap(display, minimap, Map, scroll)
    # sprite_pos = UpdatePosition(sprite_pos)
    Treeman.updatePos(arrow_key_state, t_step - t0, map_rects)
    Scuttle.updatePos(wasd_key_state, t_step - t0, map_rects)


    Treeman.updateDraw(display, minimap, scroll)
    Scuttle.updateDraw(display, minimap, scroll)


    # display.blit(animation[int(time / 10) % len(animation.keys())], Finley.pos)


    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    screen.blit(minimap, (0, 0))

    pygame.display.update()
    clock.tick(60)
    t0 = t_step
