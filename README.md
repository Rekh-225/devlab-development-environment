# DevLab — Self-Hosted Development Environment & Web Service

> **University Semester Project** · Operating Systems · Spring 2025–2026  
> Obuda University — John von Neumann Faculty of Informatics  
> BSc in Computer Science Engineering

---

## 📋 Project Overview

DevLab is a complete, production-style on-premise development environment built for a small software development team. The goal was to give developers full ownership and control over their source code, issue tracking, and corporate website — without relying on any external cloud-based hosting platforms such as GitHub or GitLab.com.

The entire stack is self-hosted on a **Microsoft Azure virtual machine** running **Ubuntu Server 24.04 LTS**, with all services configured, secured, and automated from scratch.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               DEVELOPER WORKSTATIONS (VMware)               │
│                                                             │
│  ┌─────────────────────┐    ┌─────────────────────────┐    │
│  │   winclient01        │    │   linuxclient02          │    │
│  │   Windows 11 Edu     │    │   Ubuntu Desktop 24.04   │    │
│  │   VS Code · Git CLI  │    │   VS Code · Git CLI      │    │
│  └──────────┬──────────┘    └──────────┬───────────────┘    │
└─────────────┼──────────────────────────┼────────────────────┘
              │    git push/pull          │    git pull
              └──────────────┬───────────┘
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────┐
│          MICROSOFT AZURE — Poland Central Region            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Azure NSG (Firewall) — Default Deny Inbound        │   │
│  │  Whitelist: 22, 80, 443, 3000, 19999               │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │  Ubuntu Server 24.04 LTS — 20.215.214.197           │   │
│  │  Standard_B2s_v2  (2 vCPU / 8 GB RAM / 30 GB SSD)  │   │
│  │                                                     │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────┐ │   │
│  │  │  Gitea   │ │  Nginx   │ │ dnsmasq  │ │Netdata│ │   │
│  │  │  :3000   │ │ :80/:443 │ │   :53    │ │:19999 │ │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └───────┘ │   │
│  │                                                     │   │
│  │  ┌──────────┐ ┌──────────┐ ┌─────────────────────┐ │   │
│  │  │  Flask   │ │   UFW    │ │   rsync + cron       │ │   │
│  │  │  :5000   │ │ Firewall │ │   nightly 23:00      │ │   │
│  │  └──────────┘ └──────────┘ └─────────────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Cloud | Microsoft Azure (Poland Central) | VM hosting, static public IP |
| Server OS | Ubuntu Server 24.04 LTS | All services host OS |
| Version Control | Gitea 1.22.3 | Self-hosted Git + issue tracker |
| Web Server | Nginx 1.24+ | Corporate website + reverse proxy |
| DNS | dnsmasq 2.89+ | Internal hostname resolution |
| Monitoring | Netdata (latest) | Real-time CPU/RAM/Disk/Network |
| Backup | rsync + cron | Nightly automated backup at 23:00 |
| Web App | Python Flask 3.x | Server-side unit converter |
| TLS | OpenSSL (self-signed) | HTTPS encryption |
| Firewall | Azure NSG + UFW | Dual-layer default-deny |
| Client 1 | Windows 11 Education (VMware) | Developer workstation |
| Client 2 | Ubuntu Desktop 24.04 (VMware) | Cross-platform client |
| IDE | Visual Studio Code | Development environment |
| VCS Client | Git CLI | Push/pull operations |

---

## ✅ Features Implemented

### Version Control (Gitea)
- Self-hosted Git repository server with integrated issue tracker
- Admin-only account creation — public self-registration disabled
- 2 organisations: `devlab-alpha` and `devlab-beta`
- 2 repositories: `project-alpha` and `project-beta`
- 7 user accounts with role-based access (Owner / Writer / Reader)
- Branch management: main + development + testing branches
- Issue tracking: 8 issues across both projects

### Web Server (Nginx)
- Corporate website with 4 pages (Home, Services, Contact, About Us)
- HTTPS with automatic HTTP → HTTPS redirect
- Reverse proxy for Gitea and Flask application
- Self-signed TLS certificate (RSA 2048-bit, OpenSSL)

### Web Application (Python Flask)
- Server-side unit converter application
- 8 conversion types: km/miles, Celsius/Fahrenheit, kg/lbs, metres/feet
- Accessible via `/converter` on the main website
- Runs as systemd service, proxied by Nginx

### DNS (dnsmasq)
- Internal DNS resolution for all `devlab.local` hostnames
- Records: `git.devlab.local`, `www.devlab.local`, `monitor.devlab.local`
- Google DNS (8.8.8.8) as upstream resolver

### Monitoring (Netdata)
- Real-time hardware monitoring dashboard
- Monitors: CPU utilisation, RAM usage, Disk I/O, Network throughput
- 1-second update granularity
- Browser-accessible at port 19999

### Backup Automation (rsync + cron)
- Nightly backup at 23:00 via cron
- Backs up Gitea repository data AND website files
- Separate backup directories from primary data
- Timestamped log entry written on every execution (success/failure)

### Security
- SSH: public key authentication only — password login disabled
- Dual firewall: Azure NSG + UFW with default-deny inbound
- Gitea: self-registration permanently disabled
- HTTPS: all web traffic encrypted

### Client VMs
- Windows 11 Education VM — Git push to development branch verified
- Ubuntu Desktop 24.04 VM — Git pull from development branch verified
- Both VMs in VMware Workstation Pro with NAT networking
- VS Code installed on both clients

---

## 📁 Repository Structure

```
devlab-development-environment/
│
├── README.md                          ← You are here
│
├── docs/
│   ├── DevLab_Documentation.pdf       ← Full project documentation (40+ pages)
│   └── architecture-diagram.md        ← Detailed architecture notes
│
├── configs/
│   ├── nginx-devlab.conf              ← Nginx virtual host config
│   ├── dnsmasq.conf                   ← dnsmasq DNS config
│   └── gitea-app.ini                  ← Gitea configuration (sanitised)
│
├── scripts/
│   ├── devlab-backup.sh               ← Nightly backup script
│   ├── setup-server.sh                ← Server baseline setup script
│   └── gitea-service.service          ← Gitea systemd service file
│
├── app/
│   └── app.py                         ← Python Flask unit converter
│
└── screenshots/
    ├── gitea-dashboard.png
    ├── website-https.png
    ├── netdata-dashboard.png
    ├── git-push-windows.png
    └── git-pull-linux.png
```

---

## 🚀 Key Technical Decisions

**Why Azure over local hosting?**  
Azure provides a globally accessible static IP, meaning all three team members can access the server from any location — university, home, or library — without VPN or port forwarding. The Azure for Students programme provided USD 100 free credit.

**Why Gitea over GitLab?**  
GitLab CE requires a minimum of 4 GB RAM just for itself, consuming the entire VM budget. Gitea provides all required features (Git hosting, issue tracker, role-based access, admin-only registration) using under 100 MB RAM.

**Why rsync + cron over dedicated backup software?**  
The task required a simple, auditable, scheduled backup. rsync is a battle-tested Unix tool that has been in production use since 1996. The backup script is 20 lines — easy to verify, audit, and troubleshoot.

**Why self-signed TLS over Let's Encrypt?**  
The server uses a raw IP address rather than a registered domain name. Let's Encrypt requires domain validation and cannot issue certificates for bare IP addresses. A self-signed certificate provides the same encryption quality for this use case.

---

## 👥 Team

| Name | Student ID | Role |
|------|-----------|------|
| Rehan Khaliq | EPA5RI | Infrastructure, Azure, Gitea, Nginx, Flask, DevOps |
| Shah Nawaz | GEWXHI | Web Development, Documentation |
| Danial Umer | FTBE2V | Backup Automation, Linux Client, Testing |

---

## 🎓 Academic Context

- **Institution:** Obuda University — John von Neumann Faculty of Informatics
- **Course:** Operating Systems
- **Semester:** Spring 2025–2026
- **Task:** Task 3 — Development Environment and Web Service
- **Final Score:** Full core marks + 4.8 bonus points

### Bonus Points Achieved
| Bonus | Points |
|-------|--------|
| HTTPS website with TLS | +0.6 |
| Web application with server-side computation | +2.0 |
| Monitoring dashboard (Netdata) | +1.2 |
| Cross-platform Linux client VM | +1.0 |
| **Total** | **+4.8** |

---

## 📄 License

This project was created for educational purposes as part of a university coursework assignment.  
All software components used are open-source. Configuration files and scripts in this repository are free to use and adapt.
