"""Ricart-Agrawala mutual exclusion protocol implementation."""

import json
import threading
import time
from socket import socket


class RicartAgrawala:
    def __init__(self, process_id: str, peer_id: str, connection: socket) -> None:
        self.process_id = process_id
        self.peer_id = peer_id
        self.connection = connection
        self.clock = 0
        self.requesting = False
        self.request_timestamp = 0
        self.awaiting_reply = threading.Event()
        self.deferred = False
        self.lock = threading.Lock()

    def send(self, message: dict) -> None:
        self.connection.sendall(json.dumps(message).encode())

    def receive(self, message: dict) -> None:
        with self.lock:
            self.clock = max(self.clock, message.get("clock", 0)) + 1
            if message["type"] == "reply":
                self.awaiting_reply.set()
                return
            incoming_priority = (message["clock"], message["from"])
            own_priority = (self.request_timestamp, self.process_id)
            if self.requesting and own_priority < incoming_priority:
                self.deferred = True
                return
            self.clock += 1
            self.send({"type": "reply", "from": self.process_id, "to": message["from"], "clock": self.clock})

    def request_critical_section(self) -> None:
        with self.lock:
            self.clock += 1
            self.requesting = True
            self.request_timestamp = self.clock
            self.awaiting_reply.clear()
            self.send({"type": "request", "from": self.process_id, "to": self.peer_id, "clock": self.clock})
        print("Request sent; waiting for permission...")
        self.awaiting_reply.wait()
        print("Entered critical section")
        time.sleep(2)
        print("Left critical section")
        with self.lock:
            self.requesting = False
            if self.deferred:
                self.deferred = False
                self.clock += 1
                self.send({"type": "reply", "from": self.process_id, "to": self.peer_id, "clock": self.clock})
