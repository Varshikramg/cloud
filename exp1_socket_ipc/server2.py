"""Server 2 for the socket IPC experiment."""

from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket

HOST = "127.0.0.1"
PORT = 5002


def serve() -> None:
    with socket(AF_INET, SOCK_STREAM) as server:
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server 2 listening on {HOST}:{PORT}")
        while True:
            connection, address = server.accept()
            with connection:
                print(f"Client connected: {address}")
                while data := connection.recv(1024):
                    message = data.decode().strip()
                    print(f"Client: {message}")
                    connection.sendall(f"Server 2 received: {message}".encode())


if __name__ == "__main__":
    serve()
