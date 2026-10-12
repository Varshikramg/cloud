# Experiment 7: Hypervisor Clustering in VMware

## Aim

Build a two node Proxmox VE cluster as nested VMs in VMware, configure VM replication and HA, test HAProxy load balancing, and migrate a running VM between nodes.

## Requirements

- VMware Workstation Pro and a Proxmox VE AMD64 ISO
- A host with hardware virtualization enabled and enough RAM/disk for two Proxmox VMs plus a Debian test VM
- Nested virtualization enabled for both Proxmox VMs (**VM Settings > Processors > Virtualize Intel VT-x/EPT or AMD-V/RVI**)

## Procedure

### 1. Configure VMware NAT networking

1. Open **Edit > Virtual Network Editor** as administrator.
2. Select **VMnet8**, choose **NAT**, and set subnet `192.168.94.0` with mask `255.255.255.0`.
3. In DHCP settings, set the range to `192.168.94.128` through `192.168.94.254`. Keep the NAT gateway at `192.168.94.2`.
4. Connect both Proxmox VMs to **Custom: VMnet8**. Their static addresses below are outside the DHCP range.

### 2. Install two Proxmox nodes

Create two VMware VMs named `Proxmox-01` and `Proxmox-02`. Attach the Proxmox ISO, use a bridged-free VMnet8 network, and enable nested virtualization. Install Proxmox VE on each VM using these values:

| Setting | Proxmox-01 | Proxmox-02 |
| --- | --- | --- |
| Hostname | `pve01.cloud.local` | `pve02.cloud.local` |
| Address | `192.168.94.10/24` | `192.168.94.11/24` |
| Gateway | `192.168.94.2` | `192.168.94.2` |
| DNS | `192.168.94.2` | `192.168.94.2` |

Use a strong root password and remember it. After both installs finish, open `https://192.168.94.10:8006` and `https://192.168.94.11:8006` from the host. Sign in as `root` (realm **Linux PAM**) and accept the browser's self-signed certificate warning.

### 3. Check connectivity and create the cluster

In the Proxmox-02 shell (web UI: select node > **Shell**), run:

```bash
ping -c 4 192.168.94.10
```

Confirm `0% packet loss`. Then:

1. Sign in to Proxmox-01, select **Datacenter > Cluster > Create Cluster**.
2. Enter `cloud-cluster` and click **Create**. Wait until cluster creation finishes.
3. On Proxmox-01, select **Datacenter > Cluster > Join Information** and copy the information/token.
4. On Proxmox-02, open **Datacenter > Cluster > Join Cluster**, paste the information, enter Proxmox-01's root password, and click **Join**.
5. Refresh the Proxmox-01 web UI. Under **Datacenter > Cluster**, confirm `pve01` and `pve02` are online.

### 4. Create replicated storage and a test VM

On **both** Proxmox nodes, create a ZFS pool on an unused virtual disk (do not select the disk containing Proxmox). In the node UI, open **Disks > ZFS > Create: ZFS**; select the unused disk and use pool name `replicated`. A dedicated extra virtual disk should be added to each Proxmox VM in VMware before this step.

1. Create VM **100** on `pve01`, name it `ha-test`, and install Debian. Give it a small CPU, memory, and disk allocation appropriate to your host.
2. Move VM 100's disk to the `replicated` ZFS storage using **VM 100 > Hardware > disk > Disk Action > Move Storage**.
3. Select **Datacenter > Replication > Add**, choose VM 100, target `pve02`, and a short schedule such as every minute. Click **Create** and wait for the job to finish.
4. Confirm the replication status is `OK` and `FailCount` is `0` before proceeding.

### 5. Enable HA and test recovery

1. Select **Datacenter > HA > Add**, choose VM 100, and set its desired state to `started`.
2. Test a controlled online migration first: select VM 100 > **More > Migrate**, choose `pve02`, enable **Online**, then click **Migrate**. Confirm VM 100 is running on `pve02`.
3. For a node failure demonstration, ensure replication is current. Shut down `pve02` from the Proxmox UI or VMware, then allow HA time to recover VM 100 on `pve01`.

**Two-node quorum note:** a two-node cluster may lose quorum when one node goes offline. For an isolated disposable lab only, on the surviving node you can temporarily run `pvecm expected 1`, then start/recover the VM. Do not use this workaround on a production cluster. Restore the expected vote count after both nodes return, or use a third quorum device for a proper setup.

### 6. Configure HAProxy on VM 100 (optional load-balancing task)

Inside Debian VM 100, create two backend pages on loopback:

```bash
sudo apt update
sudo apt install -y haproxy
mkdir -p ~/backend1 ~/backend2
echo 'Backend Server 1' > ~/backend1/index.html
echo 'Backend Server 2' > ~/backend2/index.html
cd ~/backend1 && python3 -m http.server 8081 --bind 127.0.0.1
```

Open another VM 100 terminal and run:

```bash
cd ~/backend2 && python3 -m http.server 8082 --bind 127.0.0.1
```

In a third terminal, back up and edit HAProxy config:

```bash
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.bak
sudo nano /etc/haproxy/haproxy.cfg
```

Keep the existing `global` and `defaults` sections. Add:

```text
frontend web_front
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    option httpchk GET /
    server backend1 127.0.0.1:8081 check
    server backend2 127.0.0.1:8082 check
```

Save and run:

```bash
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
sudo systemctl enable --now haproxy
sudo systemctl status haproxy --no-pager
```

From a fourth terminal in VM 100, send several requests:

```bash
for i in {1..6}; do curl -s http://127.0.0.1/; done
```

Responses should alternate between the backends. Stop one backend terminal with **Ctrl+C** and repeat; the other backend should continue responding. Restart the stopped backend command to restore round-robin operation.

### 7. Migrate the VM between nodes

1. Confirm both nodes are online and VM 100 is running.
2. Select VM 100 > **More > Migrate**.
3. Choose the other node as the target and enable **Online**.
4. Click **Migrate**, wait for the task to complete, and confirm VM 100 remains running on the target node.

## Expected output

- Both nodes are online in `cloud-cluster`; ping succeeds with no packet loss.
- VM 100 replication shows `State = OK` and `FailCount = 0`.
- HAProxy is `active (running)` and returns responses from both backends.
- VM 100 migrates to the other node and remains running.

## Result

A nested two-node Proxmox cluster, VM replication/HA, load balancing, and online migration were demonstrated in VMware Workstation.
