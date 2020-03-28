import time
import pygame
import math
from pygame.sprite import Group

from settings import Settings
from car import Car
from monkey import Monkey
import game_funtions as gf

def run_game():
    #Initialise pygame, settings, and screen object.
    pygame.init()
    clock = pygame.time.Clock()
    fm_settings = Settings()
    screen = pygame.display.set_mode((fm_settings.screen_width, fm_settings.screen_height))
    pygame.display.set_caption("Funky Monkeys")

    # Open music downloaded from: https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1200072
    file = 'music/hallofmountainkingopen.mp3'
    pygame.mixer.quit()
    pygame.mixer.pre_init(48000, -16, 2, 1024*3)
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    song_bpm = 111
    # milliseconds per beat
    song_mspb = (60000/song_bpm)*2

    #Make a car

    car = Car(fm_settings, screen)

    #Make car pieces

    pieces = Group()

    # Make x monkeys
    list_monkey_colors = ['blue','green','orange','pink','purple','red']
    num_monkeys = 108
    num_active_monkeys = 0
    monkeys = [Monkey(screen,list_monkey_colors[i%6]) for i in range(num_monkeys)]
    monkey_radius = 200

    monkeys[0].set_position(0,num_monkeys,monkey_radius)
    num_active_monkeys = 1

    clock.tick(30)
    previous_time = pygame.time.get_ticks()

    try:
        while True:
            gf.check_events(car)

            screen.fill(fm_settings.screen_bg_colour)

            clock.tick(40)
            current_time = pygame.time.get_ticks()
            time_passed_ms = current_time - previous_time
            previous_time = current_time

            car.update(time_passed_ms, Monkey, fm_settings, screen, pieces)
            # ACCESS NUMBER OF MONKEYS LATCHED WITH Monkey.total_latched

            if (((current_time/song_mspb)>num_active_monkeys)and(num_active_monkeys < num_monkeys)):
                num_active_monkeys += 1
                monkeys[num_active_monkeys-1].set_position(num_active_monkeys-1,num_monkeys,monkey_radius)

            for i in range(0,num_active_monkeys):
                monkeys[i].update(car,time_passed_ms)

            pieces.update()

            #get ride of old pieces
            for piece in pieces:
                if piece.rect.bottom < 0 or piece.rect.bottom > fm_settings.screen_height:
                    pieces.remove(piece)





            gf.update_screen(fm_settings, screen, car, monkeys, pieces)
    finally:
        pygame.mixer.quit() 
        print("Quitting")

run_game()