# DevLab — Architecture Notes

## Infrastructure

The DevLab environment runs on a single Microsoft Azure virtual machine
in the Poland Central region (Warsaw, Poland). This region was selected
as the geographically closest available Azure region to Budapest, Hungary
from the list permitted by the Azure for Students subscription policy.

**VM Specification:**
- Provider: Microsoft Azure
- VM Size: Standard_B2s_v2
- vCPU: 2 cores
- RAM: 8 GB
- OS Disk: 30 GB Premium SSD
- OS: Ubuntu Server 24.04 LTS
- Public IP: Static (set via Azure Portal → IP Configuration → Static)
- Region: Poland Central

## Security Architecture

Two independent firewall layers protect the server:

**Layer 1 — Azure Network Security Group (NSG)**
Controls all traffic at the cloud network perimeter. Default-deny inbound.
Whitelist rules added for ports: 22, 80, 443, 3000, 19999.

**Layer 2 — UFW (Uncomplicated Firewall)**
OS-level firewall on the Ubuntu Server. Default-deny inbound.
Whitelist rules for ports: 22, 53, 80, 443, 3000, 5000, 19999.

Both layers must permit a connection for it to reach any service.
This provides defence-in-depth — even if one layer is misconfigured,
the other continues to protect the server.

**SSH Hardening:**
- PasswordAuthentication set to 'no' in /etc/ssh/sshd_config
- Only RSA public key holders can authenticate
- The .pem key file is required for all SSH connections

## Service Architecture

All services run as systemd units and start automatically on boot:

| Service     | Unit file          | Port  | Start command                    |
|-------------|-------------------|-------|----------------------------------|
| Gitea       | gitea.service      | 3000  | systemctl enable --now gitea     |
| Nginx       | nginx.service      | 80/443| systemctl enable --now nginx     |
| dnsmasq     | dnsmasq.service    | 53    | systemctl enable --now dnsmasq   |
| Netdata     | netdata.service    | 19999 | systemctl enable --now netdata   |
| Flask App   | devlab-app.service | 5000  | systemctl enable --now devlab-app|

## Network Flow

External request → Azure NSG → UFW → Nginx (443)
                                    ├── /          → static website files
                                    ├── /git/      → proxy → Gitea (3000)
                                    ├── /converter → proxy → Flask (5000)
                                    └── /monitor/  → proxy → Netdata (19999)

Direct access (bypassing Nginx):
- Gitea:   http://SERVER_IP:3000
- Netdata: http://SERVER_IP:19999
- SSH:     ssh -i key.pem devadmin@SERVER_IP

## Backup Architecture

```
cron (23:00 daily)
    └── devlab-backup.sh
            ├── rsync /var/lib/gitea/ → /mnt/backup/gitea/
            ├── rsync /var/www/devlab/ → /mnt/backup/website/
            └── log entry → /var/log/devlab/backup.log
```

The --delete flag in rsync ensures that files deleted from the source
are also removed from the backup destination, keeping them in sync.

## Gitea Role Mapping

The task specification uses role names that differ from Gitea's built-in
permission system. The mapping used is:

| Task Role   | Gitea Permission | Access Level                              |
|-------------|-----------------|-------------------------------------------|
| Master      | Owner           | Full repository access, can manage settings|
| Developer   | Writer          | Can push code, create issues, review PRs  |
| Reporter    | Reader          | Read-only — can view code and issues only |

## Client VM Networking

Both client VMs use VMware NAT networking. NAT provides:
- Automatic internet access through the host machine's connection
- No manual IP configuration required
- Direct access to the Azure server's public IP (20.215.214.197)
- Works on any WiFi network the host laptop connects to

The VMs do not need to be on the same network as each other —
they both independently connect to the Azure server over the internet.
