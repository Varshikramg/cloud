# Distributed Systems Experiments

This repository contains four Python distributed-systems experiments. You can view any file in a terminal without cloning or downloading the repository by running its `curl.exe` command.

## View code with curl

Run these commands in PowerShell or Command Prompt. The code is printed directly in the terminal.

### Experiment 1: Socket-based client-server IPC

Objective: implement inter-process communication with sockets using two servers and two clients.

```powershell
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp1_socket_ipc/server1.py"
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp1_socket_ipc/server2.py"
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp1_socket_ipc/client1.py"
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp1_socket_ipc/client2.py"
```

To run, save the four files in an `exp1_socket_ipc` folder. Open four terminals and run these commands in this order:

```powershell
python .\exp1_socket_ipc\server1.py
python .\exp1_socket_ipc\server2.py
python .\exp1_socket_ipc\client1.py
python .\exp1_socket_ipc\client2.py
```

Type a message in either client. Type `quit` to close a client.

### Experiment 2: Remote Method Invocation (RMI)

Objective: invoke methods remotely through a socket-based client-server application.

```powershell
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp2_rmi/server.py"
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp2_rmi/client.py"
```

To run, save both files in an `exp2_rmi` folder. Open two terminals and run these commands in this order:

```powershell
python .\exp2_rmi\server.py
python .\exp2_rmi\client.py
```

The client invokes remote `add`, `multiply`, `power`, and `greet` methods.

### Experiment 3: Ricart-Agrawala distributed mutual exclusion

Objective: implement socket-based message passing and distributed mutual exclusion with the Ricart-Agrawala algorithm.

```powershell
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp3_ricart_agrawala/server.py"
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp3_ricart_agrawala/client.py"
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp3_ricart_agrawala/rechart.py"
```

To run, save all three files in the same `exp3_ricart_agrawala` folder. Open three terminals and run these commands in this order:

```powershell
python .\exp3_ricart_agrawala\server.py
python .\exp3_ricart_agrawala\client.py --id A
python .\exp3_ricart_agrawala\client.py --id B
```

After both clients are ready, press Enter in either client to request the critical section. Type `quit` to close a client.

### Experiment 4: Lamport and vector clocks

Objective: demonstrate logical clocks and vector clocks for ordering events and identifying causality.

```powershell
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp4_clocks/lamportclock.py"
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp4_clocks/vectorclock.py"
```

To run, save both files in an `exp4_clocks` folder. Run either script independently:

```powershell
python .\exp4_clocks\lamportclock.py
python .\exp4_clocks\vectorclock.py
```

## Requirement

Install Python 3.10 or later. Check it with:

```powershell
python --version
```
