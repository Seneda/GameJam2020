import time
import re
from queue import Queue, Empty
from threading import Event, Thread

import pygame.sprite

from Engine.Control import KeyState, ProcessPygameEvents
from Engine.Character import Character
from Engine.Level import Level
from Engine.Map import Map

pygame.init()
WINDOW_SIZE = (1200, 800)
WINDOW_PIXELS = (300, 200)


npc_queue = Queue()
player_queue = Queue()
kill_signal = Event()

def generate_npc_state(npc_queue, player_queue, kill_signal):
    assert isinstance(kill_signal, Event)
    while not kill_signal.is_set():
        time.sleep(0.5)
        while True:
            try:
                state = player_queue.get_nowait()
            except Empty:
                break
        npc_queue.put(state)

level = Level("test_map_new_format", "Scuttlefish", (20, 80), "Treeman", (30, 70), player_state_queue=player_queue, npc_state_queue=npc_queue)
thread = Thread(target=generate_npc_state, args=(npc_queue, player_queue, kill_signal), daemon=True)
thread.start()
level.run()
kill_signal.set()

