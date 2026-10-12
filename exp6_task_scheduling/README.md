# Experiment 6: Task Scheduling and Load Balancing

## Aim

Schedule recurring tasks on an Ubuntu VM with cron and record their output.

## Requirements

- One Ubuntu VM in VMware with an internet connection
- A terminal opened in the VM

## Procedure

### 1. Install and start cron

```bash
sudo apt update
sudo apt install -y cron
sudo systemctl enable --now cron
sudo systemctl status cron --no-pager
```

Confirm the status says `active (running)`.

### 2. Create a task script

```bash
cd ~
nano script.sh
```

Enter this script:

```bash
#!/bin/bash
echo "Scheduled run: $(date)"
echo "Host: $(hostname)"
uptime
```

Save with **Ctrl+O**, Enter, and exit with **Ctrl+X**. Make it executable and run it once:

```bash
chmod +x ~/script.sh
ls -l ~/script.sh
~/script.sh
```

### 3. Schedule the task every minute

Open your own crontab:

```bash
crontab -e
```

If prompted, select **nano**. Add this line at the bottom, replacing `your_username` with the name printed by `whoami`:

```cron
* * * * * /home/your_username/script.sh >> /home/your_username/output.log 2>&1
```

For example, if `whoami` prints `shan`, the line should be:

```cron
* * * * * /home/shan/script.sh >> /home/shan/output.log 2>&1
```

Save and exit nano. Wait one or two minutes, then check the output:

```bash
cat ~/output.log
```

### 4. Check cron's log

```bash
sudo journalctl -u cron --since "5 minutes ago" --no-pager
```

You should see the scheduled command run and new timestamps in `output.log`.

### 5. Optional: prioritize a CPU task

To compare task priority, run a CPU task at low priority:

```bash
nice -n 10 sha256sum /dev/zero
```

Stop it with **Ctrl+C**. A higher nice value gives the task lower CPU scheduling priority.

## Expected output

The log contains a new timestamp and system uptime about once per minute, and the cron journal shows the command being run.

## Result

Recurring task execution and output logging were configured and verified with cron.
