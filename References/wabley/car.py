import pygame
import math
from damage_to_jeep import Jeep_Piece
import time

class Car():

    def __init__(self, fm_settings, screen):
        """Initialise the car and set its starting position"""
        self.screen = screen


        # Load image and get its rect.
        self.orginal_image = pygame.image.load('images/car.png')

        self.width = self.orginal_image.get_width()
        self.height = self.orginal_image.get_height()

        self.screen_rect = screen.get_rect()

        self.image = self.orginal_image
        self.rect = self.image.get_rect()

        self.angle = 0.0
        self.speed = 0.1
        self.factor = 10

        # Set car in the centre of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        # Store a decimal value for ship's centre
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # Rotating flag
        self.rotating_clockwise = False
        self.rotating_anticlockwise = False
        self.forward_motion = False


    def update(self,time_passed_ms, monkey, fm_settings, screen, pieces):
        """Rotate the ship about centre point"""

        if self.speed > 0:
            self.speed = 0.1 - 0.005*monkey.total_latched
        elif self.speed <= 0 and monkey.total_latched < 20:
            self.speed = 0.1 - 0.005*monkey.total_latched
        else:
            self.speed = 0


        #create damaged pieces

        if 1 <= monkey.total_latched <= 3 :
            if self.factor % 75 == 0:
             ##create a new piece and add it to the piece group
                new_piece = Jeep_Piece(fm_settings, screen, self)
                pieces.add(new_piece)
                self.factor += 1
            else:
                self.factor += 1
        elif 3 < monkey.total_latched <= 6 :
            if self.factor % 50 == 0:
             ##create a new piece and add it to the piece group
                new_piece = Jeep_Piece(fm_settings, screen, self)
                pieces.add(new_piece)
                self.factor += 1
            else:
                self.factor += 1
        elif 7 <= monkey.total_latched <= 9:
            if self.factor % 30 == 0:
             ##create a new piece and add it to the piece group
                new_piece = Jeep_Piece(fm_settings, screen, self)
                pieces.add(new_piece)
                self.factor += 1
            else:
                self.factor += 1
        elif 10 <= monkey.total_latched:
            if self.factor % 15 == 0:
             ##create a new piece and add it to the piece group
                new_piece = Jeep_Piece(fm_settings, screen, self)
                pieces.add(new_piece)
                self.factor += 1
            else:
                self.factor += 1

        if self.forward_motion:

            if 0 <= self.angle <= 90:
                self.centerx -= float((math.sin(math.radians(self.angle))) * self.speed * time_passed_ms)
                self.centery -= float((math.cos(math.radians(self.angle))) * self.speed * time_passed_ms)

            elif 90 < self.angle <= 180:
                direction = self.angle - 90.0
                self.centery += float((math.sin(math.radians(direction))) * self.speed * time_passed_ms)
                self.centerx -= float((math.cos(math.radians(direction))) * self.speed * time_passed_ms)

            elif 180 < self.angle <= 270:
                direction = self.angle - 180.0
                self.centerx += float((math.sin(math.radians(direction))) * self.speed * time_passed_ms)
                self.centery += float((math.cos(math.radians(direction))) * self.speed * time_passed_ms)

            elif 270 < self.angle <= 360:
                direction = self.angle - 270.0
                self.centery -= float((math.sin(math.radians(direction))) * self.speed * time_passed_ms)
                self.centerx += float((math.cos(math.radians(direction))) * self.speed * time_passed_ms)
            else:
                print("No")

        if self.centerx < (self.screen_rect.left - 20):
            self.centerx = self.screen_rect.right + 20
            self.rect.centerx = round(self.centerx, 3)
            self.rect.centery = round(self.centery, 3)
        elif self.centerx > (self.screen_rect.right + 20):
            self.centerx = self.screen_rect.left - 20
            self.rect.centerx = round(self.centerx, 3)
            self.rect.centery = round(self.centery, 3)
        elif self.centery > (self.screen_rect.bottom + 20):
            self.centery = self.screen_rect.top - 20
            self.rect.centerx = round(self.centerx, 3)
            self.rect.centery = round(self.centery, 3)
        elif self.centery < (self.screen_rect.top - 20):
            self.centery = self.screen_rect.bottom + 20
            self.rect.centerx = round(self.centerx, 3)
            self.rect.centery = round(self.centery, 3)
        else:
            self.rect.centerx = round(self.centerx, 3)
            self.rect.centery = round(self.centery, 3)



        if self.rotating_clockwise:
            self.image = pygame.transform.rotate(self.orginal_image, self.angle)
            self.angle = (self.angle - 1) % 360
            x, y = self.rect.center  # Save its current center.
            self.rect = self.image.get_rect()  # Replace old rect with new rect.
            self.rect.center = (x, y)  # Put the new rect's center at old center.



        elif self.rotating_anticlockwise:
            self.image = pygame.transform.rotate(self.orginal_image, self.angle)
            self.angle = (self.angle + 1) % 360
            x, y = self.rect.center  # Save its current center.
            self.rect = self.image.get_rect()  # Replace old rect with new rect.
            self.rect.center = (x, y)  # Put the new rect's center at old center.

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
