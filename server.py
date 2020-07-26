import socket
import threading

PORT = 5050
IP = socket.gethostbyname(socket.gethostname())
HEADER = 2048
FORMAT = 'utf-8'
ADDRESS = (IP, PORT)
DISCONNECT = "quit"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDRESS)
clients = {}
addresses = {}


def handle_client(conn):
    """Handles a single client"""
    name = conn.recv(HEADER).decode(FORMAT)
    print("[CONNECTED!]")
    welcome_msg = f"Welcome {name}! To exit the chat enter [quit]"
    conn.send(bytes(welcome_msg, FORMAT))
    message = f"{name} has joined the chat!"
    send_message(message.encode(FORMAT))
    clients[conn] = name
    while True:
        msg = conn.recv(HEADER)
        if msg != DISCONNECT.encode(FORMAT):
            send_message(msg, name + ":")
        else:
            conn.send(DISCONNECT.encode(FORMAT))
            conn.close()
            del clients[conn]
            send_message(f"{name} has left the chat!".encode(FORMAT))
            break


def send_message(message, name=""):
    """Send message to all the clients"""
    for client in clients:
        client.send(bytes(name, FORMAT)+message)


def run_server():
    server.listen()
    print(f"[SERVER] is running on {IP}")

    while True:
        conn, address = server.accept()
        conn.send(bytes("Welcome! Please type your name and hit enter!", "utf-8"))
        addresses[conn] = address
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    run_server()

