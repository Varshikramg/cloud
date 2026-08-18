"""Client 1 connects to Server 1."""

from socket import AF_INET, SOCK_STREAM, socket

HOST = "127.0.0.1"
PORT = 5001


def run() -> None:
    with socket(AF_INET, SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print("Connected to Server 1. Type quit to exit.")
        while (message := input("You: ").strip()) != "quit":
            if not message:
                continue
            client.sendall(message.encode())
            print(client.recv(1024).decode())


if __name__ == "__main__":
    run()
