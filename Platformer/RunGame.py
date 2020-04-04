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


def connect_to_reomte_game(remote_queue, player_queue, kill_signal):
    while not kill_signal.is_set():
        try:
            player = player_queue.get_nowait()
            remote_queue.put(player)
        except Empty:
            pass
    print("Connection Ending")


if __name__ == '__main__':
    multiprocessing.set_start_method("spawn")
    pygame.init()
    WINDOW_SIZE = (600, 400)

    kill_signal = Event()

    chars = {
        "A": ("Treeman", (20, 80), Queue(), Queue()),
        "B": ("Scuttlefish", (40, 80), Queue(), Queue()),
        "C": ("Centiman", (60, 80), Queue(), Queue()),
        "D": ("Batman", (80, 80), Queue(), Queue()),
             }

    levela = Level(
        map_name="test_map_new_format",
        player_character_name=chars['A'][0],
        player_start_pos=chars["A"][1],
        npc_names=[chars["B"][0], chars["C"][0], chars["D"][0]],
        npc_start_positions=[chars["B"][1], chars["C"][1], chars["D"][1]],
        window_size=WINDOW_SIZE,
        player_state_queue=chars['A'][2],
        npc_state_queues=[chars["B"][3], chars["C"][3], chars["D"][3]]
    )

    levelb = Level(
        map_name="test_map_new_format",
        player_character_name=chars['B'][0],
        player_start_pos=chars["B"][1],
        npc_names=[chars["A"][0], chars["C"][0], chars["D"][0]],
        npc_start_positions=[chars["A"][1], chars["C"][1], chars["D"][1]],
        window_size=WINDOW_SIZE,
        player_state_queue=chars['B'][2],
        npc_state_queues=[chars["A"][3], chars["C"][3], chars["D"][3]]
    )

    levelc = Level(
        map_name="test_map_new_format",
        player_character_name=chars['C'][0],
        player_start_pos=chars["C"][1],
        npc_names=[chars["A"][0], chars["B"][0], chars["D"][0]],
        npc_start_positions=[chars["A"][1], chars["B"][1], chars["D"][1]],
        window_size=WINDOW_SIZE,
        player_state_queue=chars['C'][2],
        npc_state_queues=[chars["A"][3], chars["B"][3], chars["D"][3]]
    )

    leveld = Level(
        map_name="test_map_new_format",
        player_character_name=chars['D'][0],
        player_start_pos=chars["D"][1],
        npc_names=[chars["A"][0], chars["B"][0], chars["C"][0]],
        npc_start_positions=[chars["A"][1], chars["B"][1], chars["C"][1]],
        window_size=WINDOW_SIZE,
        player_state_queue=chars['D'][2],
        npc_state_queues=[chars["A"][3], chars["B"][3], chars["C"][3]]
    )

    pa = Process(target=levela.run, args=(kill_signal, 30))
    pb = Process(target=levelb.run, args=(kill_signal, 30))
    pc = Process(target=levelc.run, args=(kill_signal, 30))
    pd = Process(target=leveld.run, args=(kill_signal, 30))
    p_conn_a = Process(target=connect_to_reomte_game, args=(chars["A"][3], chars['A'][2], kill_signal))
    p_conn_b = Process(target=connect_to_reomte_game, args=(chars["B"][3], chars['B'][2], kill_signal))
    p_conn_c = Process(target=connect_to_reomte_game, args=(chars["C"][3], chars['C'][2], kill_signal))
    p_conn_d = Process(target=connect_to_reomte_game, args=(chars["D"][3], chars['D'][2], kill_signal))
    pb.start()
    pa.start()
    pc.start()
    pd.start()
    p_conn_a.start()
    p_conn_b.start()
    p_conn_c.start()
    p_conn_d.start()

    while not kill_signal.is_set():
        print("Tick", kill_signal.is_set())
        time.sleep(1)

    print("joining threads")
    pa.join()
    print("joining threads")
    pb.join()
    print("joining threads")
    pc.join()
    print("joining threads")
    pd.join()
    print("joining threads")
    p_conn_a.join()
    print("joining threads")
    p_conn_b.join()
    print("joining threads")
    p_conn_c.join()
    print("joining threads")
    p_conn_d.join()
    print("All done")
