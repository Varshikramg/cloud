"""Lamport logical clock event-ordering demonstration."""


class LamportClock:
    def __init__(self, process: str) -> None:
        self.process = process
        self.time = 0

    def internal_event(self, name: str) -> None:
        self.time += 1
        print(f"{self.process}: {name}, clock = {self.time}")

    def send_event(self, name: str) -> int:
        self.time += 1
        print(f"{self.process}: send {name}, timestamp = {self.time}")
        return self.time

    def receive_event(self, name: str, received_time: int) -> None:
        self.time = max(self.time, received_time) + 1
        print(f"{self.process}: receive {name}, clock = {self.time}")


if __name__ == "__main__":
    p1, p2 = LamportClock("P1"), LamportClock("P2")
    p1.internal_event("local event")
    timestamp = p1.send_event("m1 to P2")
    p2.internal_event("local event")
    p2.receive_event("m1", timestamp)
    reply_timestamp = p2.send_event("m2 to P1")
    p1.receive_event("m2", reply_timestamp)
