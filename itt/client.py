#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import Tkinter

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf-8")
            msg_list.insert(Tkinter.END, msg)
        except OSError: # Possibly the client has left the chat.
            break

def send(event=None): # Event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("") # Clears input field.
    client_socket.send(bytes(msg, "utf-8")) # See if removing the dash in utf8 causes a bug.
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

top = Tkinter.Tk()
top.title("Chatter")

messages_frame = Tkinter.Frame(top)
my_msg = Tkinter.StringVar() # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = Tkinter.Scrollbar(messages_frame) # To navigate through past messages.

msg_list = Tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
msg_list.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

entry_field = Tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
Tkinter.mainloop()
