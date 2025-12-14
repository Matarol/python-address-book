import socket
import threading

HEADER: int = 64
PORT: int = 5050
SERVER: str = socket.gethostbyname(socket.gethostname())
ADDR: tuple = (SERVER, PORT)
FORMAT: str = 'utf-8'
DISCONNECT_MESSAGE: str = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr) -> None:
    print(f"[NEW CONNECTION] {addr} connected.")

    connected: bool = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Message recieved".encode(FORMAT))

    conn.close()

        

def start() -> None:
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()

