import json
from _socket import SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR
from copy import copy
from pprint import pprint
from queue import Queue, Empty
from socket import socket
from threading import Thread
from time import time


class RemotePlayerConnection(object):
    def __init__(self, ip_addr=None, socket=None, char_name=None):
        self.ip_addr = ip_addr
        self.socket = socket
        self.recv_queue = Queue()
        self.send_queue = Queue()
        self.name = char_name


def sock_recv_packet(sock):
    start_char = sock.recv(1)
    while start_char != b'#':
        start_char = sock.recv(1)
    len_digits_bytes = sock.recv(1)
    len_digits_str = len_digits_bytes.decode('utf-8')
    len_digits = int(len_digits_str)
    packet_len_bytes = sock.recv(len_digits)
    packet_len_str = packet_len_bytes.decode('utf-8')
    packet_len = int(packet_len_str)
    packet_bytes = sock.recv(packet_len)
    packet_str = packet_bytes.decode("utf-8")
    packet = json.loads(packet_str)
    # print(" Received = ", packet)
    return packet


def sock_send_packet(sock, packet):
    packet_str = json.dumps(packet)
    packet_bytes = packet_str.encode("utf-8")
    packet_len_str = str(len(packet_bytes))
    packet_len_bytes = packet_len_str.encode('utf-8')
    digits_len = len(packet_len_bytes)
    digits_len_str = str(digits_len)
    digits_len_bytes = digits_len_str.encode('utf-8')
    msg_bytes = b'#' + digits_len_bytes + packet_len_bytes + packet_bytes
    # print(" Sending = ", msg_bytes.decode("utf-8"))
    sock.send(msg_bytes)


def listen_to_player(conn, send_queue):
    while True:
        packet = sock_recv_packet(conn.socket)
        send_queue.put({"name": conn.name, "packet": packet})


def send_messages(remote_connections, send_queue):
    while True:
        packet = send_queue.get()
        for conn in remote_connections:
            if packet["name"] != conn.name:
                sock_send_packet(conn.socket, packet["packet"])


def run_game_server(kill_signal, ip, port):
    print("Starting network loop as server {}".format((ip, port)))

    main_socket = socket(AF_INET, SOCK_STREAM)
    # main_socket.setdefaulttimeout(1)
    main_socket.settimeout(10)
    main_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    main_socket.bind((ip, port))
    remote_connections = []
    while True:
        main_socket.listen(1)
        print("Waiting for remote connections...")
        t0 = time()
        try:
            sock, client_address = main_socket.accept()
        except WindowsError:
            print("No more connections.")
            break
        print("Connection received from {} after {}s".format(client_address, time() - t0))
        conn = RemotePlayerConnection(client_address, sock)
        conn_info = sock_recv_packet(sock)
        conn.name = conn_info["Character"]
        remote_connections.append(conn)
        print("Server Connected")

    print("Sending game info to all players. ")
    game_info = {
        "players": [
            {"Character": conn.name} for conn in remote_connections
        ]
    }
    pprint(game_info)
    for conn in remote_connections:
        sock_send_packet(conn.socket, {
        "players": [
            {"Character": c.name} for c in remote_connections if c.name != conn.name
        ]
    })

    send_queue = Queue()
    for conn in remote_connections:
        t = Thread(name="listen to player {}".format(conn.name), target=listen_to_player, args=(conn, send_queue))
        t.start()

    send_messages(remote_connections, send_queue)


def run_server_thread(kill_signal, ip, port):
    t = Thread(name="run server", target=run_game_server, args=(kill_signal, ip, port), daemon=True)
    t.start()


def run_client_thread(kill_signal, game_info, ip, port):
    print("Starting network loop as client {}".format((ip, port)))

    ADDR = (ip, port)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(ADDR)
    # sock.setblocking(False)
    print("Client Connected")
    sock_send_packet(sock, game_info)

    game_info = sock_recv_packet(sock)
    remote_connections = [RemotePlayerConnection(socket=sock, char_name=player['Character']) for player in game_info['players']]

    recv_thread = Thread(name="Client RECV loop", target=run_recv_message_loop, args=(kill_signal, remote_connections))
    send_thread = Thread(name="Client SEND loop", target=run_send_message_loop, args=(kill_signal, remote_connections))
    recv_thread.start()
    send_thread.start()
    return remote_connections


def run_send_message_loop(kill_signal, remote_connections):
    while not kill_signal.is_set():
        for conn in remote_connections:
            assert isinstance(conn, RemotePlayerConnection)
            try:
                packet = conn.send_queue.get_nowait()
                sock_send_packet(conn.socket, packet)
            except Empty:
                pass


def run_recv_message_loop(kill_signal, remote_connections):
    while not kill_signal.is_set():
        for conn in remote_connections:
            assert isinstance(conn, RemotePlayerConnection)
            try:
                packet = sock_recv_packet(conn.socket)
                # print("Q Received ", packet)
                if packet:
                    conn.recv_queue.put(packet)
            except BlockingIOError:
                pass
