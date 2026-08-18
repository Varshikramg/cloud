"""Message relay for a two-process Ricart-Agrawala demonstration."""

import json
import threading
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket

HOST = "127.0.0.1"
PORT = 7000
clients: dict[str, socket] = {}
lock = threading.Lock()


def handle(connection: socket) -> None:
    process_id = None
    try:
        while data := connection.recv(4096):
            message = json.loads(data.decode())
            if message["type"] == "register":
                process_id = message["id"]
                with lock:
                    clients[process_id] = connection
                print(f"Process {process_id} registered")
                continue
            with lock:
                destination = clients.get(message["to"])
            if destination:
                destination.sendall(json.dumps(message).encode())
    finally:
        if process_id:
            with lock:
                clients.pop(process_id, None)
        connection.close()


def serve() -> None:
    with socket(AF_INET, SOCK_STREAM) as server:
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Ricart-Agrawala relay listening on {HOST}:{PORT}")
        while True:
            connection, _ = server.accept()
            threading.Thread(target=handle, args=(connection,), daemon=True).start()


if __name__ == "__main__":
    serve()
