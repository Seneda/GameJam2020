import argparse
import multiprocessing
import sys
import time
import re
from multiprocessing import Queue, Process, Event
from queue import Empty

import pygame.sprite


from Engine.Level import Level


# def connect_to_reomte_game(remote_queues, player_queue, kill_signal):
#     while not kill_signal.is_set():
#         try:
#             player = player_queue.get_nowait()
#             for remote_queue in remote_queues:
#                 remote_queue.put(player)
#         except Empty:
#             pass
#     print("Connection Ending")


parser = argparse.ArgumentParser()
parser.add_argument("--server", help="Set the game up in server mode, "
                                     "use this if you have forwarded a port to accept connections",
                    action="store_true", default=False)
parser.add_argument("--host-ip", help="The ip address on which the connections will be made. "
                                      "For server, use the localhost, for the client use the public ip of the server.",
                    default='localhost', )
parser.add_argument("--fps", help="The target framerate to run at",
                    default=30, type=int)
parser.add_argument("--char", help="The character to play as",
                    default="Batman", type=str)
parser.add_argument("--port", help="The ip address on which the connections will be made. "
                                      "For server, use the localhost, for the client use the public ip of the server.",
                    default=33012, type=int)
parser.add_argument("-m", "--magnification", help="The level of magnifcation to use for rendering the game",
                    default=1.5, type=int)


def main():

    args = parser.parse_args()
    level = Level(
        map_name="test_map_new_format",
        player_character_name=args.char,
        player_start_pos=(20 + 32 if args.server else 64, 80),
        window_size=(800, 400),
        magnification=args.magnification,
        server=args.server,
        host=args.host_ip,
        port=args.port,
    )
    level.run(framerate=args.fps)

    #   EXANPLE OF 4 WAY MULTIPLAYER, NOT READY TO DELETE JUST YET
    # multiprocessing.set_start_method("spawn")
    # pygame.init()
    # WINDOW_SIZE = (600, 400)
    #
    # kill_signal = Event()
    # if args.server:
    #     chars = {0: "Treeman", 1: "Batman", }
    # else:
    #     chars = {0: "Batman", 1: "Treeman", }
    #
    # char_queues = {player_idx: [Queue() for c in chars if c is not player_idx] for player_idx, player_name in chars.items()}
    #
    # remote_queues = {}
    # for player_idx in char_queues.keys():
    #     remote_queues[player_idx] = []
    #     for remote_idx, queues in char_queues.items():
    #         if remote_idx != player_idx:
    #             remote_queues[player_idx].append(queues[player_idx%len(chars)-1])
    #
    # levels = [Level(
    #     map_name="test_map_new_format",
    #     player_character_name=player_name,
    #     player_start_pos=(20 + player_idx * 32, 80),
    #     npc_names=[npc_name for npc_idx, npc_name in chars.items() if player_name != npc_name],
    #     npc_start_positions=[(20 + npc_idx * 320, 80) for npc_idx, npc_name in chars.items() if player_name != npc_name],
    #     window_size=WINDOW_SIZE,
    #     player_state_queue=char_queues[player_idx],
    #     npc_state_queues=remote_queues[player_idx],
    #     server=args.server,
    # ) for player_idx, player_name in chars.items()]
    #
    # processes = [Process(target=level.run, args=(kill_signal, 60)) for level in levels]
    #
    # for proc in processes:
    #     proc.start()
    #
    # while not kill_signal.is_set():
    #     print("Tick", kill_signal.is_set())
    #     time.sleep(1)


if __name__=="__main__":
    main()
