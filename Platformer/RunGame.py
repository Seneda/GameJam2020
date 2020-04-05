import multiprocessing
import sys
import time
import re
from multiprocessing import Queue, Process, Event
from queue import Empty

import pygame.sprite

from Engine.Level import Level


def connect_to_reomte_game(remote_queues, player_queue, kill_signal):
    while not kill_signal.is_set():
        try:
            player = player_queue.get_nowait()
            for remote_queue in remote_queues:
                remote_queue.put(player)
        except Empty:
            pass
    print("Connection Ending")

def main():
    multiprocessing.set_start_method("spawn")
    pygame.init()
    WINDOW_SIZE = (600, 400)

    kill_signal = Event()

    chars = {0: "Treeman", 1: "Scuttlefish", }

    char_queues = {player_idx: [Queue() for c in chars if c is not player_idx] for player_idx, player_name in chars.items()}

    remote_queues = {}
    for player_idx in char_queues.keys():
        remote_queues[player_idx] = []
        for remote_idx, queues in char_queues.items():
            if remote_idx != player_idx:
                remote_queues[player_idx].append(queues[player_idx%len(chars)-1])

    levels = [Level(
        map_name="test_map_new_format",
        player_character_name=player_name,
        player_start_pos=(20 + player_idx * 32, 80),
        npc_names=[npc_name for npc_idx, npc_name in chars.items() if player_name != npc_name],
        npc_start_positions=[(20 + npc_idx * 320, 80) for npc_idx, npc_name in chars.items() if player_name != npc_name],
        window_size=WINDOW_SIZE,
        player_state_queue=char_queues[player_idx],
        npc_state_queues=remote_queues[player_idx]
    ) for player_idx, player_name in chars.items()]

    processes = [Process(target=level.run, args=(kill_signal, 60)) for level in levels]

    for proc in processes:
        proc.start()

    while not kill_signal.is_set():
        print("Tick", kill_signal.is_set())
        time.sleep(1)

if __name__=="__main__":
    level = Level(
        map_name="test_map_new_format",
        player_character_name="Treeman",
        player_start_pos=(20 + 32, 80),
        npc_names=["Batman"],
        npc_start_positions=[(20 + 64, 80) ],
        window_size=(800, 400),
        player_state_queue=[Queue()],
        npc_state_queues=[Queue()],
        server=True,
    )
    level.run()