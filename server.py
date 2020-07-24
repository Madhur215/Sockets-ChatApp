import socket
import select
import threading

PORT = 5050
IP = socket.gethostbyname(socket.gethostname())
HEADER = 64
FORMAT = 'utf-8'
ADDRESS = (IP, PORT)
DISCONNECT = "quit"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDRESS)
clients_list = []


def handle_client(conn, address):
    print("[CONNECTED!]")
    connected = True
    while connected:
        try:
            message = conn.recv(2048)
            if message:
                print(address[0] + ">> " + "message")
                if message == DISCONNECT:
                    connected = False
                send_message(message, conn)
        except:
            continue
    conn.close()


def send_message(message, conn):
    for client in clients_list:
        if client != conn:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)


def remove(conn):
    if conn in clients_list:
        clients_list.remove(conn)


def run_server():
    server.listen()
    print(f"[SERVER] is running on {IP}")

    while True:
        conn, address = server.accept()
        clients_list.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

