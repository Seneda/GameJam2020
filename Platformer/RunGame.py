import multiprocessing
import time
import re
from multiprocessing import Queue, Process, Event
from queue import Empty

import pygame.sprite

from Engine.Control import KeyState, ProcessPygameEvents
from Engine.Character import Character
from Engine.Level import Level
from Engine.Map import Map


def connect_to_reomte_game(game_a_npc_queue, game_b_player_queue, kill_signal):
    while not kill_signal.is_set():
        try:
            player = game_b_player_queue.get_nowait()
            game_a_npc_queue.put(player)
        except Empty:
            pass
    print("Connection Ending")


if __name__ == '__main__':
    multiprocessing.set_start_method("spawn")
    pygame.init()
    WINDOW_SIZE = (600, 400)

    game_a_player_queue = Queue()
    game_a_npc_queue = Queue()
    game_b_player_queue = Queue()
    game_b_npc_queue = Queue()
    kill_signal = Event()

    # def generate_npc_state(npc_queue, player_queue, kill_signal):
    #     assert isinstance(kill_signal, Event)
    #     while not kill_signal.is_set():
    #         time.sleep(2)
    #         while True:
    #             try:
    #                 state = player_queue.get_nowait()
    #             except Empty:
    #                 break
    #         npc_queue.put(state)
    #     print("Kill signal received, ending.")

    levela = Level(
        map_name="test_map_new_format",
        player_character_name="Scuttlefish",
        player_start_pos=(20, 80),
        npc_name="Treeman",
        npc_start_pos=(30, 70),
        window_size=WINDOW_SIZE,
        player_state_queue=game_a_player_queue,
        npc_state_queue=game_a_npc_queue
    )

    levelb = Level(
        map_name="test_map_new_format",
        player_character_name="Treeman",
        player_start_pos=(30, 80),
        npc_name="Scuttlefish",
        npc_start_pos=(20, 70),
        window_size=WINDOW_SIZE,
        player_state_queue=game_b_player_queue,
        npc_state_queue=game_b_npc_queue
    )

    pa = Process(target=levela.run, args=(kill_signal, 100))
    pb = Process(target=levelb.run, args=(kill_signal, 10))
    p_conn_a = Process(target=connect_to_reomte_game, args=(game_a_npc_queue, game_b_player_queue, kill_signal))
    p_conn_b = Process(target=connect_to_reomte_game, args=(game_b_npc_queue, game_a_player_queue, kill_signal))
    pb.start()
    pa.start()
    p_conn_a.start()
    p_conn_b.start()

    while not kill_signal.is_set():
        print("Tick", kill_signal.is_set())
        time.sleep(1)
    print("joining threads")
    pa.join()
    print("joining threads")
    pb.join()
    print("joining threads")
    p_conn_a.join()
    print("joining threads")
    p_conn_b.join()
    print("All done")
