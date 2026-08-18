# Distributed Systems Socket Experiments

Small, runnable Python examples for common distributed-systems laboratory exercises. All programs use only the Python standard library.

## Requirements

- Python 3.10 or later
- Open a terminal in this repository

## Run commands

### Experiment 1: Socket-based client-server IPC

Open four terminals and run:

```powershell
python .\exp1_socket_ipc\server1.py
python .\exp1_socket_ipc\server2.py
python .\exp1_socket_ipc\client1.py
python .\exp1_socket_ipc\client2.py
```

Each client connects to its matching server. Type messages and use `quit` to close the client.

### Experiment 2: Remote Method Invocation (RMI)

Open two terminals and run:

```powershell
python .\exp2_rmi\server.py
python .\exp2_rmi\client.py
```

The client invokes remote `add`, `multiply`, `power`, and `greet` methods exposed by the server.

### Experiment 3: Ricart-Agrawala distributed mutual exclusion

Open three terminals and run:

```powershell
python .\exp3_ricart_agrawala\server.py
python .\exp3_ricart_agrawala\client.py --id A
python .\exp3_ricart_agrawala\client.py --id B
```

In each client, press Enter to request the critical section or type `quit`. The relay server forwards the Ricart-Agrawala request/reply messages.

### Experiment 4: Logical and vector clocks

```powershell
python .\exp4_clocks\lamportclock.py
python .\exp4_clocks\vectorclock.py
```

Both scripts print a small event trace showing how the clock values change.
