import re
from queue import Empty

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
        self.window_size = window_size
        self.magnification = magnification
        self.map_name = map_name

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size, 0, 32)
        self.display = pygame.Surface((int(self.window_size[0] / self.magnification), int(self.window_size[1] / self.magnification)))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 50)
        LoadSprites()
        self.map = Map(self.map_name)
        self.minimap = pygame.Surface(self.map.size)

        self.scroll = [0, 0]
        self.scroll[0] = self.player.x - self.display.get_width() / 2
        self.scroll[1] = self.player.y - self.display.get_height() * 2 / 3


        
        arrow_key_state = KeyState()
        wasd_key_state = KeyState()
        controllers = [0, 1]
        key_states = [arrow_key_state, wasd_key_state]
        num_players = 2
        
        # create mutable var_player_state or later population
        var_player_states = [[0] * 4 for i in range(num_players)]

        t0 = time()

        # For tracking avg framerate
        totalFrameRate = 0
        countFrameRate = 0
        
        while True:  # game loop
            t_step = time()
        
            # Read in the other character's positions: 
            # Format will be x,y,x_speed,y_speed
            if self.npc_state_queue:
                while True:
                    try:
                        state = self.npc_state_queue.get_nowait()
                        self.npc.state = state
                    except Empty:
                        break
        
            game_state, key_states = ProcessPygameEvents(controllers, key_states)
            if game_state.get('Exit'):
                # Exiting
                pygame.quit()
                return

            self.display.fill(([0, 0, 0]))
            self.minimap.fill([0, 0, 0])
            self.minimap.set_colorkey((0, 0, 0))
        
            self.scroll[0] = self.scroll[0] + ((self.player.x - self.display.get_width() / 2) - self.scroll[0]) / 5
            self.scroll[1] = self.scroll[1] + ((self.player.y - 2 * self.display.get_height() / 3) - self.scroll[1]) / 10

            map_rects = self.map.draw(self.display, self.minimap, self.scroll)
            
            width_to_filter = self.display.get_width() / 2 # best guess at distance a player could feasibly move in a frame (either side)
            height_to_filter = self.display.get_height() / 2
            x_limits = [self.player.x-width_to_filter,self.player.x+width_to_filter]
            y_limits = [self.player.y-height_to_filter,self.player.y+height_to_filter]
            relevant_map_rects = [rect for rect in map_rects if ((rect.x < x_limits[1])and(rect.x > x_limits[0])and(rect.y < y_limits[1])and(rect.y > y_limits[0]))]

            self.player.updatePos(t_step - t0, relevant_map_rects, arrow_key_state)

            x_limits = [self.npc.x-width_to_filter,self.npc.x+width_to_filter]
            y_limits = [self.npc.y-height_to_filter,self.npc.y+height_to_filter]
            relevant_map_rects = [rect for rect in map_rects if ((rect.x < x_limits[1])and(rect.x > x_limits[0])and(rect.y < y_limits[1])and(rect.y > y_limits[0]))]
            
            self.npc.updatePos(t_step - t0, relevant_map_rects, None)
        
            self.player_state_queue.put(self.player.state)

            self.npc.updateDraw(self.display, self.minimap, self.scroll)
            self.player.updateDraw(self.display, self.minimap, self.scroll)
        
            self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_width(), self.screen.get_height())), (0, 0))
            self.screen.blit(pygame.transform.scale(self.minimap, (int(self.map.size[0] / 4), int(self.map.size[1] / 4))), (0, 0))

            frameRate = int(self.clock.get_fps());
            totalFrameRate += frameRate;
            countFrameRate += 1;
            if (countFrameRate > 100):
                avgFrameRate = totalFrameRate/countFrameRate
                print("average frameRate: " +str(avgFrameRate))
                totalFrameRate = 0
                countFrameRate = 0

            self.screen.blit(self.font.render("{:d} fps".format(frameRate), 1, pygame.Color("black")), (10, 50))
            pygame.display.update()
            self.clock.tick(60)
            t0 = t_step
