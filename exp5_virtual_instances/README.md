# Experiment 5: Virtual Instances, Consolidation, and Fault Tolerance
## Aim
Create two Ubuntu virtual machines in VMware, serve web pages from both, distribute requests with HAProxy, consolidate the test workload, and recover the web page from a backup VM.
## Procedure
### 1. Create the two VMs
### 2. Install Apache and make each page identifiable(vm setup)

Run these commands on **both** VMs:

```bash
sudo apt update
sudo apt install apache2 -y
sudo systemctl enable apache2
sudo systemctl status apache2
sudo nano /var/www/html/index.html
scroll down change the heading into clone 1
ifconfig
```

From the host browser, open `http://VM1_IP` and `http://VM2_IP`. Each should show its matching text.

### 3. Install and configure HAProxy on VM3(loadbalancing)

On VM3:

```bash
sudo apt install -y haproxy
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.bak
sudo nano /etc/haproxy/haproxy.cfg
```
Keep the existing `global` and `defaults` sections. Add this at the end, replacing the two IP placeholders with the addresses you recorded:
```text
frontend http_front
    bind *:8080
    default_backend http_servers

backend http_back
    balance roundrobin
    server vm1 VM1_IP:80 check
    server vm2 VM2_IP:80 check
```

In nano, save with **Ctrl+O**, Enter, then exit with **Ctrl+X**. Validate and start HAProxy:

```bash
sudo systemctl restart haproxy
sudo systemctl enable haproxy
sudo systemctl status haproxy
ifconfig
```
Open `http://VM1_IP:8080` several times. The response should alternate between VM1 and VM2. Stop Apache on VM1 to check failover, then restart it:


### 4. Demonstrate consolidation(server consoldation)

Keep both VMs running together on the same VMware host. HAProxy and one Apache backend run on VM1; the second Apache backend runs on VM2. This demonstrates consolidating several virtual workloads on one physical host while sharing requests between VMs. Confirm both pages are reachable through `http://VM1_IP:8080`.
create 2 vms and set them up using (apache2,mysql-server)
sudo apt update
'''
sudo apt install mysql-server -y
sudo systemctl enable mysql-server
'''
take screenshots of 2 vms settings
delete vm2
come to vm1
install mysql-server in vm1
take screenshot of stettings vm1
thats it 




3)FAULY TOLERENCE

ON HOST VM

sudo apt install rsync openssh-server -y
mkdir -p source
nano s.txt

ON ANOTHER VM
sudo apt install rsync openssh-server -y
sudo systemctl enable --now ssh
hostname -I  #NOTE
whoami    #NOTE
mkdir -p backup
cat ~/backup/s.txt
cat backup/source/s.txt

THEN CONTINUE ON HOST VM

rsync -av ~/source whoami_response@hostname-I_response:~/backup
cd source
rsync -av ~/source whoami_response@hostname-I_response:~/backup






