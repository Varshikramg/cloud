"""Client that invokes methods on the RMI server."""

import json
from socket import AF_INET, SOCK_STREAM, socket

HOST = "127.0.0.1"
PORT = 6000


def remote_call(method: str, *args: object) -> object:
    request = json.dumps({"method": method, "args": args}).encode()
    with socket(AF_INET, SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(request)
        response = json.loads(client.recv(4096).decode())
    if not response["ok"]:
        raise RuntimeError(response["error"])
    return response["result"]


if __name__ == "__main__":
    print("add(12, 8) =", remote_call("add", 12, 8))
    print("multiply(6, 7) =", remote_call("multiply", 6, 7))
    print("power(2, 10) =", remote_call("power", 2, 10))
    print("greet('Student') =", remote_call("greet", "Student"))
