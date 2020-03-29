import re
from queue import Queue, Empty

import pygame
from time import time

from Engine.Character import Character
from Engine.Control import KeyState, ProcessPygameEvents
from Engine.Map import Map
from Engine.Sprites import LoadSprites


class Level(object):
    def __init__(self, map_name, player_character_name, player_start_pos, npc_name, npc_start_pos, window_size=(800, 400), magnification=2, player_state_queue=None, npc_state_queue=None):
        self.player = Character(player_character_name, player_start_pos)
        self.npc = Character(npc_name, npc_start_pos)
        self.player_state_queue = player_state_queue
        self.npc_state_queue = npc_state_queue


        self.screen = pygame.display.set_mode(window_size, 0, 32)
        self.map = Map(map_name)
        LoadSprites()
        self.display = pygame.Surface((int(window_size[0]/magnification), int(window_size[1]/magnification)))
        self.minimap = pygame.Surface(self.map.size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 50)
        
        self.scroll = [0, 0]
        self.scroll[0] = self.player.x - self.display.get_width() / 2
        self.scroll[1] = self.player.y - self.display.get_height() * 2 / 3

    def run(self):        
        
        arrow_key_state = KeyState()
        wasd_key_state = KeyState()
        controllers = [0, 1]
        key_states = [arrow_key_state, wasd_key_state]
        num_players = 2
        
        # create mutable var_player_state or later population
        var_player_states = [[0] * 4 for i in range(num_players)]

        t0 = time()
        
        while True:  # game loop
            t_step = time()
        
            # Read in the other character's positions: 
            # Format will be x,y,x_speed,y_speed
            if self.npc_state_queue:
                assert isinstance(self.npc_state_queue, Queue)
                while True:
                    try:
                        state = self.npc_state_queue.get_nowait()
                        self.npc.state = state
                    except Empty:
                        break
        
            game_state, key_states = ProcessPygameEvents(controllers, key_states)
            if game_state.get('Exit'):
                pygame.quit()
                return

            self.display.fill(([0, 0, 0]))
            self.minimap.fill([0, 0, 0])
            self.minimap.set_colorkey((0, 0, 0))
        
            self.scroll[0] = self.scroll[0] + ((self.player.x - self.display.get_width() / 2) - self.scroll[0]) / 5
            self.scroll[1] = self.scroll[1] + ((self.player.y - 2 * self.display.get_height() / 3) - self.scroll[1]) / 10
        
            map_rects = self.map.draw(self.display, self.minimap, self.scroll)
        
            self.player.updatePos(t_step - t0, map_rects, arrow_key_state)
            self.npc.updatePos(t_step - t0, map_rects, None)
        
            self.player_state_queue.put(self.player.state)

            self.npc.updateDraw(self.display, self.minimap, self.scroll)
            self.player.updateDraw(self.display, self.minimap, self.scroll)
        
            self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_width(), self.screen.get_height())), (0, 0))
            self.screen.blit(pygame.transform.scale(self.minimap, (int(self.map.size[0] / 4), int(self.map.size[1] / 4))), (0, 0))

            self.screen.blit(self.font.render("{:d} fps".format(int(self.clock.get_fps())), 1, pygame.Color("black")), (10, 50))
            pygame.display.update()
            self.clock.tick(60)
            t0 = t_step