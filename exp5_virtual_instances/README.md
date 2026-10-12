# Experiment 5: Virtual Instances, Consolidation, and Fault Tolerance
## Aim
Create two Ubuntu virtual machines in VMware, serve web pages from both, distribute requests with HAProxy, consolidate the test workload, and recover the web page from a backup VM.
## Procedure
### 1. Create the two VMs
### 2. Install Apache and make each page identifiable

Run these commands on **both** VMs:

```bash
sudo apt update
sudo apt install apache2 -y
sudo systemctl enable apache2
sudo systemctl status apache2
sudo nano /var/www/html/index.html
ifconfig
```

On VM1, set its page:

```bash
echo "VM 1 - Apache web server" | sudo tee /var/www/html/index.html
```

On VM2:

```bash
echo "VM 2 - Apache web server" | sudo tee /var/www/html/index.html
```

From the host browser, open `http://VM1_IP` and `http://VM2_IP`. Each should show its matching text.

### 3. Install and configure HAProxy on VM3

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


### 4. Demonstrate consolidation

Keep both VMs running together on the same VMware host. HAProxy and one Apache backend run on VM1; the second Apache backend runs on VM2. This demonstrates consolidating several virtual workloads on one physical host while sharing requests between VMs. Confirm both pages are reachable through `http://VM1_IP:8080`.

### 5. Prepare a backup VM and demonstrate recovery

1. In VMware, shut down VM1 and choose **VM > Manage > Clone** (or create another Ubuntu VM named `VM1-Backup`). Connect it to VMnet8 and start it.
2. On VM1-Backup, install Apache and create the recovery page:

   ```bash
   sudo apt update
   sudo apt install -y apache2
   echo "VM 1 backup page" | sudo tee /var/www/html/index.html
   sudo systemctl enable --now apache2
   hostname -I
   ```

3. Verify `http://VM1_BACKUP_IP` from the host browser.
4. To simulate VM1 failure, shut down VM1 in VMware. Open `http://VM1_BACKUP_IP`; the backup page should remain available. This is a manual recovery demonstration, not automatic failover.

## Expected output

- VM1 and VM2 each display their own Apache page.
- HAProxy is `active (running)` and requests are served by both backends.
- When one backend is stopped, the other continues responding.
- With VM1 powered off, the backup VM's page is available.

## Result

Virtual instances, basic load balancing, workload consolidation, and backup-based recovery were demonstrated.
