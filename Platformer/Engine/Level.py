import re
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from multiprocessing import Event
from queue import Empty
from random import random
from threading import Thread

import pygame
import pygame.locals
from time import time, sleep

from Engine.Character import Character
from Engine.Control import KeyState, ProcessPygameEvents
from Engine.Map import Map
from Engine.Sprites import LoadSprites

HOST = 'localhost'
PORT = 12342
BUFSIZE = 1024

class Level(object):
    def __init__(self, map_name, player_character_name, player_start_pos, npc_names=(), npc_start_positions=(),
                 window_size=(800, 400), magnification=2, player_state_queue=None, npc_state_queues=None, enable_minimap=True, server=False):
        self.player = Character(player_character_name, player_start_pos)
        # print("Player: ", self.player)
        self.npcs = [Character(npc_names[i], npc_start_positions[i]) for i in range(len(npc_names))]
        # print("NPCs : ", self.npcs)
        self.player_state_queues = player_state_queue
        self.npc_state_queues = npc_state_queues
        self.window_size = window_size
        self.magnification = magnification
        self.map_name = map_name
        self.enable_minimap = enable_minimap
        self.server = server

        # print(self.player)

    def run_server_thread(self, kill_signal):
        print("Starting network loop as {}".format("server" if self.server else "client"))

        self.sockets = []
        for npc in self.npcs:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.settimeout(5)
            # sock.bind(('192.168.1.65', PORT))
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.bind(('localhost', PORT))
            sock.listen(5)
            sock, client_address = sock.accept()
            sock.setblocking(0)
            # sock.setblocking(False)
            print("Connection from", client_address)
            self.sockets.append(sock)
            print("Server Connected")

        self.run_message_loop(kill_signal)


    def run_client_thread(self, kill_signal):
        print("Starting network loop as {}".format("server" if self.server else "client"))

        ADDR = (HOST, PORT)
        self.sockets = []
        for q in self.npcs:
            sock = socket(AF_INET, SOCK_STREAM)
            # sock.setblocking(False)
            self.sockets.append(socket(AF_INET, SOCK_STREAM))
        for sock in self.sockets:
            sock.connect(ADDR)
            sock.setblocking(0)
            print("Client Connected")

        self.run_message_loop(kill_signal)

    def run_message_loop(self, kill_signal):
        while not kill_signal.is_set():
            for i, q in enumerate(self.player_state_queues):
                try:
                    msg = str(q.get_nowait())
                    print("Sending ", msg)
                    self.sockets[i].send(msg.encode())
                except Empty:
                    pass
            for i, npc in enumerate(self.npc_state_queues):
                try:
                    msg = self.sockets[i].recv(BUFSIZE).decode("utf8")
                    if msg:
                        try:
                            pos = msg.split(')')[0]
                            if pos.startswith('('):
                                pos = pos[1:]
                            pos = pos.split(', ')
                            if len(pos) == 5:
                                npc.put([float(p) for p in pos[1:]])

                            print("Message Recvd = ", pos)
                        except:
                            print("Exception")
                            pass
                except BlockingIOError:
                    pass

    def run(self, kill_signal=None, framerate=60):
        print("Running game {}, {}".format(self.player.name, self.map_name))
        if kill_signal is None:
            kill_signal = Event()
        pygame.init()
        pygame.event.set_allowed([pygame.locals.QUIT, pygame.locals.KEYDOWN, pygame.locals.KEYUP])
        if self.server:
            thread = Thread(target=self.run_server_thread, args=(kill_signal,), daemon=True)
        else:
            thread = Thread(target=self.run_client_thread, args=(kill_signal,), daemon=True)

        thread.start()
        flags =  pygame.locals.DOUBLEBUF
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

            for i in range(len(self.npc_state_queues)):
                # Read in the other character's positions:
                # Format will be x,y,x_speed,y_speed
                if self.npc_state_queues[i]:
                    while not kill_signal.is_set():
                        try:
                            state = self.npc_state_queues[i].get_nowait()
                            self.npcs[i].state = state
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

            self.player.updatePos(t_step - t0, relevant_map_rects, arrow_key_state)
            
            for npc in self.npcs:
                x_limits = [npc.x-width_to_filter,npc.x+width_to_filter]
                y_limits = [npc.y-height_to_filter,npc.y+height_to_filter]
                relevant_map_rects = [rect for rect in map_rects if ((rect.x < x_limits[1])and(rect.x > x_limits[0])and(rect.y < y_limits[1])and(rect.y > y_limits[0]))]
                npc.updatePos(t_step - t0, relevant_map_rects, None)
        
            if random() >= 0.0:
                if (frame_count % 2) == 0:
                    # print("Sending State ", frame_count, *self.player.state)
                    for player_state_queue in self.player_state_queues:
                        player_state_queue.put((frame_count, *self.player.state))

            for character in self.npcs + [self.player]:
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
