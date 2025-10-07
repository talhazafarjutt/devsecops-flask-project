# DevSecOps Flask Project - Deployment Guide

## Prerequisites

- Ubuntu 20.04+ server
- Domain name pointing to server IP
- Root access to server

## Quick Deployment

1. **Clone repository on server:**
   ```bash
   git clone https://github.com/talhazafarjutt/devsecops-flask-project.git
   cd devsecops-flask-project
   ```

2. **Run deployment script:**
   ```bash
   chmod +x scripts/deploy.sh
   sudo ./scripts/deploy.sh
   ```

## Manual Deployment

### 1. Install Dependencies
```bash
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx docker.io docker-compose
```

### 2. Start Services
```bash
docker-compose up -d
```

### 3. Configure Nginx
```bash
sudo cp nginx/nginx.conf /etc/nginx/sites-available/devsecops
sudo ln -s /etc/nginx/sites-available/devsecops /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Get SSL Certificate
```bash
sudo certbot --nginx -d dev.devsecopsassignment.work.gd
```

### 5. Configure Firewall
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 5001/tcp
sudo ufw deny 3000/tcp
sudo ufw deny 9090/tcp
sudo ufw --force enable
```

## Access URLs

- **Flask App**: https://dev.devsecopsassignment.work.gd
- **Grafana**: https://dev.devsecopsassignment.work.gd/grafana/
- **Prometheus**: https://dev.devsecopsassignment.work.gd/prometheus/

## Troubleshooting

### Check Container Status
```bash
docker-compose ps
docker-compose logs -f
```

### Check Nginx Status
```bash
sudo systemctl status nginx
sudo nginx -t
```

### Check SSL Certificate
```bash
sudo certbot certificates
```

### Restart Services
```bash
docker-compose restart
sudo systemctl restart nginx
```
