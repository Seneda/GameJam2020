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


npc_queue = Queue()
player_queue = Queue()
kill_signal = Event()

def generate_npc_state(npc_queue, player_queue, kill_signal):
    assert isinstance(kill_signal, Event)
    while not kill_signal.is_set():
        time.sleep(2)
        while True:
            try:
                state = player_queue.get_nowait()
            except Empty:
                break
        npc_queue.put(state)
    print("Kill signal received, ending.")

level = Level(
    map_name="test_map_new_format",
    player_character_name="Scuttlefish",
    player_start_pos=(20, 80),
    npc_name="Treeman",
    npc_start_pos=(30, 70),
    window_size=WINDOW_SIZE,
    player_state_queue=player_queue,
    npc_state_queue=npc_queue
)
thread = Thread(target=generate_npc_state, args=(npc_queue, player_queue, kill_signal), daemon=True)
thread.start()
level.run()
print("Sending kill signal")
kill_signal.set()
print("Done")

