import sys
from random import random

import pygame
import pygame.locals

pygame.init()
WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
display = pygame.Surface((300, 200))
clock = pygame.time.Clock()

r = 0
g = 0
b = 0
while True:  # game loop
    for event in pygame.event.get(): # event loop
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()

    r += random()*1 * (random() > 0.5)
    g += random()*1 * (random() > 0.5)
    b += random()*1 * (random() > 0.5)
    r = max(50, r)
    g = max(50, g)
    b = max(50, b)
    r %= 255
    g %= 255
    b %= 255

    display.fill((r, g, b))  # clear screen by filling it with blue
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)
