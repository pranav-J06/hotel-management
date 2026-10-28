#!/usr/bin/env bash
# ==============================================================================
# 1-Click AWS Lightsail / EC2 Setup Script for Hotel Management System
# Supports: Ubuntu 20.04 / 22.04 / 24.04 LTS
# ==============================================================================

set -e

echo "🚀 [1/5] Setting up 2GB Swap Memory (prevents OOM on Free-Tier / Micro instances)..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 2G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "✓ Swap configured successfully."
else
    echo "✓ Swap already exists."
fi

echo "📦 [2/5] Updating packages and installing prerequisites..."
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release git

echo "🐳 [3/5] Installing Docker and Docker Compose..."
if ! command -v docker &> /dev/null; then
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg --yes
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -y
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo usermod -aG docker "$USER"
    sudo systemctl enable docker
    sudo systemctl start docker
    echo "✓ Docker installed."
else
    echo "✓ Docker is already installed."
fi

echo "🏗️ [4/5] Building and starting all services (MySQL, Java Backend, React Frontend)..."
sudo docker compose down --remove-orphans 2>/dev/null || true
sudo docker compose up -d --build

echo "⏳ [5/5] Waiting for services to become healthy..."
sleep 15
sudo docker compose ps

# Fetch Public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com || curl -s ifconfig.me || echo "your-server-ip")

echo "=============================================================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "Your Hotel Management System is live at:"
echo "👉 http://${PUBLIC_IP}"
echo ""
echo "API Health Check:"
echo "👉 http://${PUBLIC_IP}/api/health"
echo "=============================================================================="
