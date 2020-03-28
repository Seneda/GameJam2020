import pygame
from pygame.sprite import Sprite
import random

class Jeep_Piece(Sprite):
    """A Class to manage broken pieces from the jeep"""

    def __init__(self, fm_settings, screen, car):
        """Create a broken piece object at the ship's current position."""
        super(Jeep_Piece, self).__init__()
        self.screen = screen


        #Create a broken piece at (0, 0) and then set the correct position
        self.rect = pygame.Rect(0, 0, fm_settings.jeep_piece_width, fm_settings.jeep_piece_height)
        self.rect.centerx = car.rect.centerx
        self.rect.centery = car.rect.centery
        
        #store the piece's position as a float
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.x_random = random.uniform(-1, 1)
        self.y_random = random.uniform(-1, 1)
        
        self.colour = fm_settings.jeep_piece_colour
        self.speed_factor = fm_settings.jeep_piece_speed_factor

    def update(self):
        """Move the piece in a random direction"""

        #create a random x velocity
       
        if self.x_random < 0:
            x_speed = self.x_random - 1
        else:
            x_speed = self.x_random + 1
        self.x += self.speed_factor * x_speed
        self.rect.x = round(self.x, 3)
        
        #creare a random y velocity

        if self.y_random < 0:
            y_speed = self.y_random - 1
        else:
            y_speed = self.y_random + 1
        self.y += self.speed_factor * y_speed
        self.rect.y = round(self.y, 3)
        
    def draw_piece(self):
        """Draw piece to the screen"""
        pygame.draw.rect(self.screen, self.colour, self.rect)
            