#!/bin/bash
# =============================================================================
# DevLab Nightly Backup Script
# =============================================================================
# Purpose:   Backs up Gitea repository data and corporate website files
# Schedule:  Runs automatically every night at 23:00 via cron
# Log:       /var/log/devlab/backup.log
#
# Cron entry:
#   0 23 * * * /usr/local/bin/devlab-backup.sh
# =============================================================================

# ── Configuration ─────────────────────────────────────────────────────────────
GITEA_SOURCE="/var/lib/gitea/"
GITEA_DEST="/mnt/backup/gitea/"
WEBSITE_SOURCE="/var/www/devlab/"
WEBSITE_DEST="/mnt/backup/website/"
LOG="/var/log/devlab/backup.log"

# ── Helpers ───────────────────────────────────────────────────────────────────
DATE=$(date '+%Y-%m-%d %H:%M:%S')
log() { echo "[$DATE] $1" >> "$LOG"; }

# ── Start ─────────────────────────────────────────────────────────────────────
log "========================================"
log "DevLab backup started"

# ── Step 1: Backup Gitea data ─────────────────────────────────────────────────
log "Backing up Gitea repositories..."
rsync -av --delete "$GITEA_SOURCE" "$GITEA_DEST" >> "$LOG" 2>&1

if [ $? -eq 0 ]; then
    log "Gitea backup SUCCESS"
else
    log "Gitea backup FAILED — check rsync output above"
fi

# ── Step 2: Backup website files ──────────────────────────────────────────────
log "Backing up website files..."
rsync -av --delete "$WEBSITE_SOURCE" "$WEBSITE_DEST" >> "$LOG" 2>&1

if [ $? -eq 0 ]; then
    log "Website backup SUCCESS"
else
    log "Website backup FAILED — check rsync output above"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
log "DevLab backup completed"
log "========================================"
