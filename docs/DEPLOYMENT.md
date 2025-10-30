# Deployment Guide

## Deployment Options

### Option 1: Railway (Recommended for MVP)

Railway is a modern platform for deploying applications with zero configuration.

#### Steps:

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Connect Repository**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `aim_bot` repository

3. **Configure Environment Variables**
   - Add all variables from `.env.example`
   - Set `DATABASE_URL` to PostgreSQL connection string (Railway provides this)

4. **Deploy**
   - Railway automatically detects Python and deploys
   - Bot will start automatically

#### Cost:
- Free tier: $5 credit/month
- Paid tier: ~$10-20/month

---

### Option 2: VPS (DigitalOcean, Hetzner, etc.)

For more control and potentially lower costs.

#### Steps:

1. **Create VPS**
   - OS: Ubuntu 22.04 LTS
   - Specs: 2GB RAM, 1 CPU (minimum)

2. **Connect via SSH**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install Dependencies**
   ```bash
   apt update && apt upgrade -y
   apt install python3.10 python3-pip python3-venv git -y
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/cooldog631-ai/aim_bot.git
   cd aim_bot
   ```

5. **Setup Project**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env  # Add your values
   ```

7. **Initialize Database**
   ```bash
   python scripts/init_db.py
   ```

8. **Create Systemd Service**

   Create `/etc/systemd/system/aim_bot.service`:

   ```ini
   [Unit]
   Description=AI Voice Reports Bot
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/aim_bot
   Environment="PATH=/root/aim_bot/venv/bin"
   ExecStart=/root/aim_bot/venv/bin/python src/main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

9. **Start Service**
   ```bash
   systemctl daemon-reload
   systemctl enable aim_bot
   systemctl start aim_bot
   systemctl status aim_bot
   ```

10. **View Logs**
    ```bash
    journalctl -u aim_bot -f
    ```

---

### Option 3: Docker

#### Build Image

```bash
make docker-build
```

#### Run Container

```bash
docker run -d \
  --name aim_bot \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  aim_bot:latest
```

#### Docker Compose

```bash
make docker-up
```

---

## Database Options

### SQLite (Development)
- Default, no setup needed
- File-based: `aim_bot.db`
- Not recommended for production

### PostgreSQL (Production)

#### Railway:
- Automatically provided
- Set `DATABASE_URL` in environment

#### Manual Setup:
```bash
# Install PostgreSQL
apt install postgresql postgresql-contrib -y

# Create database
sudo -u postgres psql
CREATE DATABASE aim_bot;
CREATE USER aim_bot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE aim_bot TO aim_bot_user;
\q

# Update .env
DATABASE_URL=postgresql://aim_bot_user:your_password@localhost:5432/aim_bot
```

---

## Monitoring

### Logs

Logs are stored in `logs/` directory:
- `aim_bot.log`: All logs
- `errors.log`: Errors only

### Health Checks

API health endpoint:
```bash
curl http://localhost:8000/health
```

Bot health:
```bash
systemctl status aim_bot
```

---

## Backup Strategy

### Database Backup

SQLite:
```bash
cp aim_bot.db aim_bot.db.backup
```

PostgreSQL:
```bash
pg_dump aim_bot > aim_bot_backup.sql
```

### Automated Backups

Add to crontab:
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup_script.sh
```

---

## Security Checklist

- [ ] Change default passwords
- [ ] Enable firewall (ufw)
- [ ] Use HTTPS for API (nginx + Let's Encrypt)
- [ ] Restrict database access
- [ ] Enable bot token rotation
- [ ] Set up monitoring alerts
- [ ] Regular security updates

---

## Scaling Considerations

### Horizontal Scaling
- Multiple bot instances with load balancer
- Shared PostgreSQL database
- Redis for session storage

### Vertical Scaling
- Increase VPS resources
- Optimize database queries
- Enable caching

---

## Troubleshooting

### Bot Not Starting
1. Check logs: `journalctl -u aim_bot -f`
2. Verify environment variables
3. Test database connection

### High Memory Usage
1. Check for memory leaks
2. Limit concurrent operations
3. Increase swap space

### Database Connection Issues
1. Verify DATABASE_URL
2. Check PostgreSQL service
3. Review connection pool settings

---

## Cost Estimates

### Railway
- $10-20/month (with PostgreSQL)

### VPS
- DigitalOcean: $6-12/month
- Hetzner: €4-8/month

### API Services
- OpenAI Whisper: ~$0.006/minute
- OpenAI GPT-4: ~$0.03/1K tokens
- Anthropic Claude: ~$0.015/1K tokens

### Total Monthly Cost (50 users, 20 reports/day)
- Hosting: $10-20
- AI APIs: $50-100
- **Total: ~$60-120/month**
