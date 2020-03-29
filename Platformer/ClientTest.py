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
            print(msg)
        except OSError:  # Possibly client has left the chat.
            break


def send():  # event is passed by binders.
    """Handles sending of messages."""
    msg = "Blah"
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    # my_msg.set("{quit}")
    # send()



#----Now comes the sockets part----
HOST = '192.168.1.65'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

while True:
    print("Sending")
    send()