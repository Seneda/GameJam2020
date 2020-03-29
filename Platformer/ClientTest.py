#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(time.time()-1585501100, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send():  # event is passed by binders.
    """Handles sending of messages."""
    msg = "245,876"
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    # my_msg.set("{quit}")
    # send()



#----Now comes the sockets part----
HOST = '80.189.136.21'
PORT = 33012
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

for i in range(0, 2):
    print("Sending")
    t0 = time.time() - 1585501100
    print("t0", i, t0)
    send()
