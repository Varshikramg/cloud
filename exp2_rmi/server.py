"""Minimal JSON-over-sockets Remote Method Invocation server."""

import json
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket

HOST = "127.0.0.1"
PORT = 6000


def invoke(method: str, arguments: list[object]) -> object:
    methods = {
        "add": lambda a, b: a + b,
        "multiply": lambda a, b: a * b,
        "power": lambda a, b: a**b,
        "greet": lambda name: f"Hello, {name}!",
    }
    if method not in methods:
        raise ValueError(f"Unknown remote method: {method}")
    return methods[method](*arguments)


def serve() -> None:
    with socket(AF_INET, SOCK_STREAM) as server:
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"RMI server listening on {HOST}:{PORT}")
        while True:
            connection, address = server.accept()
            with connection:
                print(f"Client connected: {address}")
                request = json.loads(connection.recv(4096).decode())
                try:
                    response = {"ok": True, "result": invoke(request["method"], request["args"])}
                except (KeyError, TypeError, ValueError) as error:
                    response = {"ok": False, "error": str(error)}
                connection.sendall(json.dumps(response).encode())


if __name__ == "__main__":
    serve()
