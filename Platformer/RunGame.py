import os
import sys
from pprint import pprint
from random import random

import pygame
import pygame.locals

from Character import Character

pygame.init()
WINDOW_SIZE = (600, 400)
SPRITES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "sprites")

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
display = pygame.Surface((300, 200))
clock = pygame.time.Clock()


def LoadSprites():
    print("Loading Sprites...")
    sprites = {}
    for _, sprite_dirs, _ in os.walk(SPRITES_DIR):
        for sprite_name in sprite_dirs:
            print("Loading {}".format(sprite_name))
            sprites.setdefault(sprite_name, {})
            for _, _, animation_files in os.walk(os.path.join(SPRITES_DIR, sprite_name)):
                for animation_name in animation_files:
                    try:
                        print("Loading {}".format(animation_name))
                        print(animation_name)
                        animation_type = animation_name.split('_')[0]
                        animation_num = animation_name.split('_')[1].replace('.png', '')
                        sprites[sprite_name].setdefault(animation_type, {})[int(animation_num)] = pygame.image.load(
                            os.path.join(SPRITES_DIR, sprite_name, animation_name))
                    except:
                        print("Couldn't load {}".format(animation_name))
    pprint(sprites)
    return sprites

sprites = LoadSprites()
key_state = {"Up": False, "Down": False, "Left": False, "Right": False}

background_color = (100, 100, 100)
time = 0
sprite_pos = [50, 50]

animation = sprites['Centiman']['walk']

def ProcessPygameEvents(key_state):

    for event in pygame.event.get(): # event loop
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

def UpdatePosition(sprite_pos):
    speed = 1
    if key_state['Right']:
        sprite_pos[0] += speed
    if key_state['Left']:
        sprite_pos[0] -= speed
    if key_state['Down']:
        sprite_pos[1] += speed
    if key_state['Up']:
        sprite_pos[1] -= speed
    return sprite_pos

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


Finley = Character(screen,'Finley',[50,100])
Scuttle = Character(screen,'Scuttlefish',[70,100])

# Loading in floor
# floor = pygame.Rect(300,10,100,100)
floor = pygame.Rect(0,150,600,10)

while True:  # game loop
    time += 1
    key_state = ProcessPygameEvents(key_state)

    # sprite_pos = UpdatePosition(sprite_pos)
    Finley.updatePos(key_state,1,floor)
    Scuttle.updatePos(key_state,1,floor)

    background_color = UpdateBackgroundColour(background_color)
    

    display.fill(background_color)  # clear screen by filling it with blue


    # display.blit(sprites['Finley']['walk'][int(time / 10) % len(sprites['Finley']['walk'].keys())], sprite_pos)
    Finley.updateDraw(display)
    Scuttle.updateDraw(display)
    pygame.draw.rect(display, (0, 255, 0), floor)

    # display.blit(animation[int(time / 10) % len(animation.keys())], Finley.pos)

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    

    pygame.display.update()
    clock.tick(60)
