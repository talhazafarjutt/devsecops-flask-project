#!/bin/bash

# DevSecOps Flask Project - Deployment Script
set -e

echo "🚀 Starting DevSecOps Flask Project Deployment..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
apt update

# Install required packages
echo "🔧 Installing required packages..."
apt install -y nginx certbot python3-certbot-nginx docker.io docker-compose

# Start Docker
echo "🐳 Starting Docker..."
systemctl start docker
systemctl enable docker

# Navigate to project directory
cd ~/projects/devsecops-flask-project

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down || true

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Start containers
echo "🚀 Starting containers..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Configure Nginx
echo "🌐 Configuring Nginx..."
cp nginx/nginx.conf /etc/nginx/sites-available/devsecops
ln -sf /etc/nginx/sites-available/devsecops /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# Get SSL certificate if not exists
if [ ! -f "/etc/letsencrypt/live/dev.devsecopsassignment.work.gd/fullchain.pem" ]; then
    echo "🔒 Obtaining SSL certificate..."
    certbot --nginx -d dev.devsecopsassignment.work.gd --non-interactive --agree-tos --email zafartalhajutt@gmail.com
fi

# Restart Nginx
echo "🔄 Restarting Nginx..."
systemctl restart nginx

# Configure firewall
echo "🔥 Configuring firewall..."
ufw allow 80/tcp
ufw allow 443/tcp
ufw deny 5001/tcp
ufw deny 3000/tcp
ufw deny 9090/tcp
ufw deny 9100/tcp
ufw deny 8080/tcp
ufw allow from 127.0.0.1 to any port 5001
ufw allow from 127.0.0.1 to any port 3000
ufw allow from 127.0.0.1 to any port 9090
ufw --force enable

# Health check
echo "🏥 Performing health check..."
sleep 10

# Test services
curl -f http://localhost:5001 || echo "❌ Flask app not responding"
curl -f http://localhost:3000 || echo "❌ Grafana not responding"
curl -f http://localhost:9090 || echo "❌ Prometheus not responding"

# Test HTTPS
curl -f https://dev.devsecopsassignment.work.gd || echo "❌ HTTPS not working"

echo "✅ Deployment completed successfully!"
echo "🌐 Flask App: https://dev.devsecopsassignment.work.gd"
echo "📊 Grafana: https://dev.devsecopsassignment.work.gd/grafana/"
echo "📈 Prometheus: https://dev.devsecopsassignment.work.gd/prometheus/"
