# Distributed Systems Experiments

This repository contains seven cloud and distributed-systems experiments. Experiments 1-4 contain Python programs; experiments 5-7 are VMware/Ubuntu/Proxmox lab procedures.

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

## VMware lab procedures

These experiments use virtual machines and terminal commands rather than Python source files. Follow each separate procedure file:

- [Experiment 5: Virtual instances, consolidation, and fault tolerance](exp5_virtual_instances/README.md)
- [Experiment 6: Task scheduling and load balancing](exp6_task_scheduling/README.md)
- [Experiment 7: Hypervisor clustering](exp7_hypervisor_clustering/README.md)

To print any procedure in the terminal, run its command from PowerShell or Command Prompt:

### Experiment 5

```powershell
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp5_virtual_instances/README.md"
```

### Experiment 6

```powershell
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp6_task_scheduling/README.md"
```

### Experiment 7

```powershell
curl.exe --ssl-no-revoke -L "https://raw.githubusercontent.com/Varshikramg/cloud/main/exp7_hypervisor_clustering/README.md"
```
