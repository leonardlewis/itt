# https://www.geeksforgeeks.org/simple-chat-room-using-python/
# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170

#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# A loop that waits for incoming connections. New connections get logged, a
# welcome message gets printed, then the client addresses gets added to the
# addresses dictionary.

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome!" + "Please type your name, then press Enter/Return.", "utf-8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(5) # Listen for 5 connections max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start() # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
