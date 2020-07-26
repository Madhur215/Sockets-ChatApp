import threading
import tkinter as tk
import socket

PORT = 5050
IP = socket.gethostbyname(socket.gethostname())
HEADER = 2048
FORMAT = 'utf-8'
ADDRESS = (IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect(ADDRESS)


def receive_message():
    """Handles the receiving of incoming messages for each client"""

    while True:
        try:
            msg = client.recv(HEADER).decode(FORMAT)
            msg_list.insert(tk.END, msg);
        except OSError:
            break


def send_message(event=None):
    """To Handle sending of messages by the client"""
    msg = message_field.get()
    message_field.set("")
    client.send(msg.encode(FORMAT))
    if msg == "quit":
        client.close()
        root.quit()


def close_window(event=None):
    message_field.set("quit")
    send_message()


root = tk.Tk()
root.title("PyChat")

frame = tk.Frame(root)
message_field = tk.StringVar()
message_field.set("Type your message here!")
scrollbar = tk.Scrollbar(frame)
msg_list = tk.Listbox(frame, height=25, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
frame.pack()

entry_field = tk.Entry(root, textvariable=message_field)
entry_field.bind("<Return>", send_message)
entry_field.pack()
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

root.protocol("WM_DELETE_WINDOW", close_window)

thread = threading.Thread(target=receive_message)
thread.start()
tk.mainloop()

