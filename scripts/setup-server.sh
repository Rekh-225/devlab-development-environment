#!/bin/bash
# =============================================================================
# DevLab Server Baseline Setup Script
# =============================================================================
# Purpose:   Installs and configures all required packages on a fresh
#            Ubuntu Server 24.04 LTS instance
# Usage:     sudo bash setup-server.sh
# =============================================================================

set -e  # Exit immediately on error

echo "=========================================="
echo " DevLab Server Setup"
echo " Ubuntu Server 24.04 LTS"
echo "=========================================="

# ── 1. System update ──────────────────────────────────────────────────────────
echo "[1/7] Updating system packages..."
apt update && apt full-upgrade -y

# ── 2. Install required packages ──────────────────────────────────────────────
echo "[2/7] Installing required packages..."
apt install -y \
    git \
    curl \
    wget \
    nano \
    ufw \
    nginx \
    dnsmasq \
    openssl \
    netdata \
    python3-flask \
    rsync \
    cron

# ── 3. Configure UFW firewall ─────────────────────────────────────────────────
echo "[3/7] Configuring UFW firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 3000/tcp  # Gitea
ufw allow 19999/tcp # Netdata
ufw allow 53        # DNS
ufw --force enable
echo "UFW status:"
ufw status

# ── 4. Harden SSH ─────────────────────────────────────────────────────────────
echo "[4/7] Hardening SSH..."
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh
echo "SSH password authentication disabled."

# ── 5. Create Gitea user and directories ──────────────────────────────────────
echo "[5/7] Creating Gitea user and directories..."
adduser --system --shell /bin/bash --group --disabled-password --home /home/gitea gitea
mkdir -p /var/lib/gitea/{custom,data,log}
chown -R gitea:gitea /var/lib/gitea/
mkdir -p /etc/gitea
chown root:gitea /etc/gitea
chmod 770 /etc/gitea

# ── 6. Create backup directories ──────────────────────────────────────────────
echo "[6/7] Creating backup directories..."
mkdir -p /mnt/backup/gitea
mkdir -p /mnt/backup/website
mkdir -p /var/log/devlab

# ── 7. Create website directory ───────────────────────────────────────────────
echo "[7/7] Creating website directories..."
mkdir -p /var/www/devlab
mkdir -p /var/www/devlab-app
chown -R www-data:www-data /var/www/devlab

echo ""
echo "=========================================="
echo " Baseline setup complete!"
echo " Next steps:"
echo "   1. Download and install Gitea binary"
echo "   2. Configure Nginx (/etc/nginx/sites-available/devlab)"
echo "   3. Generate TLS certificate with OpenSSL"
echo "   4. Configure dnsmasq (/etc/dnsmasq.conf)"
echo "   5. Deploy Flask app (/var/www/devlab-app/app.py)"
echo "   6. Schedule backup cron job"
echo "=========================================="
