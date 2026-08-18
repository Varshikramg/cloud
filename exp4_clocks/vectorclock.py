"""Vector clock causality demonstration for two processes."""


class VectorClock:
    def __init__(self, process: str, index: int, size: int = 2) -> None:
        self.process = process
        self.index = index
        self.clock = [0] * size

    def internal_event(self, name: str) -> None:
        self.clock[self.index] += 1
        print(f"{self.process}: {name}, clock = {self.clock}")

    def send_event(self, name: str) -> list[int]:
        self.clock[self.index] += 1
        timestamp = self.clock.copy()
        print(f"{self.process}: send {name}, timestamp = {timestamp}")
        return timestamp

    def receive_event(self, name: str, received_clock: list[int]) -> None:
        self.clock = [max(local, received) for local, received in zip(self.clock, received_clock)]
        self.clock[self.index] += 1
        print(f"{self.process}: receive {name}, clock = {self.clock}")


if __name__ == "__main__":
    p1, p2 = VectorClock("P1", 0), VectorClock("P2", 1)
    p1.internal_event("local event")
    timestamp = p1.send_event("m1 to P2")
    p2.internal_event("local event")
    p2.receive_event("m1", timestamp)
    reply_timestamp = p2.send_event("m2 to P1")
    p1.receive_event("m2", reply_timestamp)
