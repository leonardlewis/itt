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
# Creates a socket object and specifies IP addresses from the internet and type SOCK_STREAM.
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
        client.send(bytes("Welcome! Please type your name, then press Enter/Return.", "utf-8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf-8")
    welcome = f"Welcome {name}! If you ever want to quit, type {quit} to exit."
    client.send(bytes(welcome, "utf-8"))
    msg = "%s has joined the chat!" % name
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes(f"{quit}", "utf-8"):
            broadcast(msg, name+": ")
        else:
            client.send.bytes(f"{quit}", "utf-8")
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf-8"))
            break

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
