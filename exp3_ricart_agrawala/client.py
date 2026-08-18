"""Run as process A or B in the Ricart-Agrawala experiment."""

import argparse
import json
import threading
from socket import AF_INET, SOCK_STREAM, socket

from rechart import RicartAgrawala

HOST = "127.0.0.1"
PORT = 7000


def receive_messages(connection: socket, protocol: RicartAgrawala) -> None:
    while data := connection.recv(4096):
        protocol.receive(json.loads(data.decode()))


def run(process_id: str) -> None:
    peer_id = "B" if process_id == "A" else "A"
    with socket(AF_INET, SOCK_STREAM) as connection:
        connection.connect((HOST, PORT))
        connection.sendall(json.dumps({"type": "register", "id": process_id}).encode())
        protocol = RicartAgrawala(process_id, peer_id, connection)
        threading.Thread(target=receive_messages, args=(connection, protocol), daemon=True).start()
        print(f"Process {process_id} ready. Press Enter to request the critical section; type quit to exit.")
        while input().strip().lower() != "quit":
            threading.Thread(target=protocol.request_critical_section, daemon=True).start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", choices=("A", "B"), required=True, help="Process identifier")
    run(parser.parse_args().id)
