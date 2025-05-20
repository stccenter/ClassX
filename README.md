# ClassX: Installation and Setup Guide for Linux Users

## 1. Introduction

This guide explains how to install and configure **ClassX**, an AI-powered web platform developed by NASA’s STC Center to support researchers in labeling and analyzing Arctic sea ice and solar image data. The system uses Docker containers for easy deployment.

### ClassX Components

- **Frontend**: React + Vite
- **Backend**: Flask API
- **Database**: MySQL
- **Authentication**: Keycloak
- **Task Queue**: Celery + Redis
- **Segmentation Model**: Mask-RCNN

---

## 2. System Requirements

Ensure your system has the following versions (or newer):

| Tool             | Version            |
|------------------|--------------------|
| Git              | 2.34.1             |
| Docker Engine    | 28.1.1             |
| Docker Compose   | v2.35.1            |

---

## 3. Install Prerequisites

Run the following commands with `sudo` (or use `sudo su -l` first):

```bash
# Step 1: Update packages
sudo apt update

# Step 2: Install base packages
sudo apt install -y git docker.io docker-compose-plugin make

# Step 3: Add Docker repository
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"${UBUNTU_CODENAME:-$VERSION_CODENAME}\") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

# Step 4: Install Docker packages
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Step 5: Enable and start Docker
sudo systemctl enable docker
sudo systemctl start docker
