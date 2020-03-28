import os
import pygame

from Platformer.Sprites import sprites


class Character():
    def __init__(self, screen, name, pos):
        """Initialise the monkey and set its starting position"""
        self.screen = screen
        self.name = name

        #Load image and get its rect.
        # self.image = pygame.image.load('../sprites/' +name +'_walk' +'.png')
        # self.rect = self.image.get_rect()
        # self.screen_rect = screen.get_rect()

        self.centerxfloat = 0
        self.centeryfloat = 0
        # self.rect.centerx = 0
        # self.rect.centery = 0

        self.speed = [0,0] # speed in x,y notation (right and up)
        self.pos = pos


    def updatePos(self, key_state, time_passed_ms, floor):
        acceleration = 0.1
        jump_speed = 1
        gravity = 10

        if key_state['Right']:
            self.speed[0] += (acceleration) * (time_passed_ms)
        if key_state['Left']:
            self.speed[0] -= (acceleration) * (time_passed_ms)
        if key_state['Down']:
            self.speed[1] += (acceleration) * (time_passed_ms)
        if key_state['Up']:
            self.speed[1] = -jump_speed

        # floor_group = [floor]
        # if pygame.sprite.spritecollideany(self, floor_group)
        #     self.speed[1] = 0

        # self.speed[1] += gravity*time_passed_ms

        self.pos[1] = self.pos[1] + self.speed[1]
        self.rect = pygame.Rect(*self.pos, 32, 32)
        while any([self.rect.colliderect(r) for r in floor]):
            for r in floor:
                while self.rect.colliderect(r):
                    self.pos[1] -= 1
                    self.rect = pygame.Rect(*self.pos, 32, 32)

        self.pos[0] = self.pos[0] + self.speed[0]
        self.rect = pygame.Rect(*self.pos, 32, 32)
        while any([self.rect.colliderect(r) for r in floor]):
            for r in floor:
                while self.rect.colliderect(r):
                    self.pos[0] -= 1
                    self.rect = pygame.Rect(*self.pos, 32, 32)



    def updateDraw(self, display):
        display.blit(sprites[self.name]['walk'][0], self.pos)

