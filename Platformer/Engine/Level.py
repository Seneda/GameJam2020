import re
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from multiprocessing import Event
from queue import Empty
from random import random
from threading import Thread

import pygame
import pygame.locals
from time import time, sleep

from Engine.Character import NormalCharacter, DoubleJumpCharacter, load_character
from Engine.Control import KeyState, ProcessPygameEvents
from Engine.Map import Map
from Engine.Network import run_client_thread, run_server_thread
from Engine.Sprites import LoadSprites

BUFSIZE = 1024

class Level(object):
    def __init__(self, map_name, player_character_name, player_start_pos,
                 window_size=(800, 400), magnification=1,
                 enable_minimap=True, server=False, host='localhost', port=12345):
        self.player = load_character(player_character_name, player_start_pos)

        self.window_size = window_size
        self.magnification = magnification
        self.map_name = map_name
        self.enable_minimap = enable_minimap
        self.server = server
        self.host_ip = host
        self.port = port

        # print(self.player)

    def run(self, kill_signal=None, framerate=60):
        try:
            print("Running game {}, {}".format(self.player.name, self.map_name))
            if kill_signal is None:
                kill_signal = Event()
            pygame.init()
            pygame.event.set_allowed([pygame.locals.QUIT, pygame.locals.KEYDOWN, pygame.locals.KEYUP])

            if self.server:
                run_server_thread(kill_signal, self.host_ip, self.port)

            game_info = {"Character": self.player.name}
            remote_connections = run_client_thread(kill_signal, game_info, self.host_ip, self.port)
            self.npcs = {conn.name: load_character(conn.name, self.player.pos) for conn in remote_connections}

            flags = pygame.locals.DOUBLEBUF
            self.screen = pygame.display.set_mode(self.window_size, flags, 32)
            if self.magnification != 1:
                self.display = pygame.Surface((int(self.window_size[0] / self.magnification), int(self.window_size[1] / self.magnification)))
            else:
                self.display = self.screen
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont('Arial', 50)
            LoadSprites()
            self.map = Map(self.map_name)
            if self.enable_minimap:
                self.minimap = pygame.Surface(self.map.size)
            else:
                self.minimap = None


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
            frame_count = 0
            while not kill_signal.is_set():  # game loop
                frame_count += 1
                t_step = time()

                if remote_connections:
                    while not kill_signal.is_set():
                        try:
                            packet = remote_connections[0].recv_queue.get_nowait()
                            if packet:
                                self.npcs[packet['Character']].state = packet['state']
                        except Empty:
                            break

                game_state, key_states = ProcessPygameEvents(controllers, key_states)
                if game_state.get('Exit'):
                    # Exiting
                    pygame.quit()
                    break

                self.display.fill(([0, 0, 0]))
                if self.minimap is not None:
                    self.minimap.fill([0, 0, 0])
                    self.minimap.set_colorkey((0, 0, 0))

                self.scroll[0] = self.scroll[0] + ((self.player.x - self.display.get_width() / 2) - self.scroll[0]) / 5
                self.scroll[1] = self.scroll[1] + (
                            (self.player.y - 2 * self.display.get_height() / 3) - self.scroll[1]) / 5


                map_rects = self.map.draw(self.display, self.minimap, self.scroll)

                width_to_filter = self.display.get_width() / 2 # best guess at distance a player could feasibly move in a frame (either side)
                height_to_filter = self.display.get_height() / 2
                x_limits = [self.player.x-width_to_filter,self.player.x+width_to_filter]
                y_limits = [self.player.y-height_to_filter,self.player.y+height_to_filter]
                relevant_map_rects = [rect for rect in map_rects if ((rect.x < x_limits[1])and(rect.x > x_limits[0])and(rect.y < y_limits[1])and(rect.y > y_limits[0]))]

                self.player.updateState(t_step - t0, relevant_map_rects, arrow_key_state)

                for npc in self.npcs.values():
                    x_limits = [npc.x-width_to_filter,npc.x+width_to_filter]
                    y_limits = [npc.y-height_to_filter,npc.y+height_to_filter]
                    relevant_map_rects = [rect for rect in map_rects if ((rect.x < x_limits[1])and(rect.x > x_limits[0])and(rect.y < y_limits[1])and(rect.y > y_limits[0]))]
                    npc.updateState(t_step - t0, relevant_map_rects, None)

                if random() >= 0.0:
                    if (frame_count % 2) == 0:
                        # print("Sending State ", frame_count, *self.player.state)
                        for conn in remote_connections:
                            conn.send_queue.put({"Character": self.player.name, "state": self.player.state})

                for character in list(self.npcs.values()) + [self.player]:
                    character.updateDraw(self.display, self.minimap, self.scroll)

                if self.magnification != 1:
                    self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_width(), self.screen.get_height())), (0, 0))
                self.screen.blit(
                    pygame.transform.scale(self.minimap, (int(self.map.size[0] / 4), int(self.map.size[1] / 4))), (0, 0))

                # frameRate = int(self.clock.get_fps());
                # totalFrameRate += frameRate;
                # countFrameRate += 1;
                # if (countFrameRate > 100):
                #     avgFrameRate = totalFrameRate/countFrameRate
                #     print("average frameRate: " +str(avgFrameRate))
                #     totalFrameRate = 0
                #     countFrameRate = 0

                self.screen.blit(self.font.render("{:d} fps".format(int(self.clock.get_fps())), 1, pygame.Color("black")),
                                 (10, 50))
                pygame.display.update()
                self.clock.tick(framerate)
                t0 = t_step
            print("Game Over, Player={}".format(self.player.name))
            if not kill_signal.is_set():
                kill_signal.set()
        except KeyboardInterrupt:
            kill_signal.set()
