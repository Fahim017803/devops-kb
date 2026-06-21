# DevOps Hub — Fresh EC2 Setup Guide

This is the full runbook for setting up DevOps Hub on a **brand new EC2 instance** —
use this if the old instance was deleted, or you're setting up a second one.

---

## 1. Launch the EC2 instance

In the AWS Console:

- **AMI:** Ubuntu Server 22.04 LTS (or newer)
- **Instance type:** t2.micro or t3.small (free tier eligible)
- **Region:** ap-northeast-1 (Tokyo) — or wherever you prefer
- **Key pair:** create new or reuse an existing `.pem` key
- **Security group — inbound rules:**
  | Type  | Port | Source    | Why                          |
  |-------|------|-----------|-------------------------------|
  | SSH   | 22   | My IP     | so you can connect            |
  | HTTP  | 80   | 0.0.0.0/0 | so the public can reach the site |
  | HTTPS | 443  | 0.0.0.0/0 | if you add SSL later          |

After launch, note the **Public IPv4 address** — this is what visitors will use
(e.g. `3.104.36.60`). This changes every time you stop/start the instance unless
you attach an Elastic IP.

---

## 2. Connect to the instance

```bash
chmod 400 ~/Downloads/your-key.pem
ssh -i ~/Downloads/your-key.pem ubuntu@<NEW_PUBLIC_IP>
```

---

## 3. Install Docker and Docker Compose

```bash
# Update package list
sudo apt-get update -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Let your user run docker without sudo
sudo usermod -aG docker ubuntu

# Apply the group change without logging out (or just SSH back in again)
newgrp docker

# Verify
docker --version
docker compose version
```

> If `docker compose version` fails, Docker Compose v2 is usually already bundled
> with modern Docker installs as `docker compose` (no hyphen). If it's missing,
> install the plugin: `sudo apt-get install docker-compose-plugin -y`

---

## 4. Install Git

```bash
sudo apt-get install git -y
git --version
```

---

## 5. Clone the project

```bash
cd ~
git clone https://github.com/Fahim017803/devops-kb.git
cd devops-kb
```

---

## 6. Create the `.env` file

The repo does **not** include `.env` (it's gitignored for security). Create it manually:

```bash
nano .env
```

Paste this in (adjust if your real credentials differ):

```
DB_HOST=db
DB_USER=devops_user
DB_PASSWORD=devops_pass
DB_NAME=devops_kb
```

Save with `Ctrl+O`, `Enter`, then exit with `Ctrl+X`.

---

## 7. Build and start everything

```bash
docker compose up -d --build
```

This builds and starts three containers:
- `devops_kb_db` — MySQL 8.0, auto-seeded from `db/init.sql` on first run
- `devops_kb_backend` — Flask API
- `devops_kb_nginx` — serves the frontend and reverse-proxies `/api/*` to Flask

---

## 8. Verify everything is running

```bash
# All 3 containers should show "Up"
docker ps

# Health check — should return {"status": "ok"} or similar
curl http://localhost/api/health

# Should return JSON with your articles
curl http://localhost/api/articles
```

Open `http://<NEW_PUBLIC_IP>/index.html` in a browser to confirm the site loads.

---

## 9. Set up the GitHub Actions self-hosted runner (if using CI/CD)

Only needed if you want `git push` to auto-deploy.

```bash
mkdir -p ~/CI-CD/actions-runner && cd ~/CI-CD/actions-runner

# Get the exact download command + token from:
# GitHub repo → Settings → Actions → Runners → New self-hosted runner
# It will look like this (token changes every time, copy it fresh):
curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/download/<VERSION>/actions-runner-linux-x64-<VERSION>.tar.gz
tar xzf ./actions-runner-linux-x64.tar.gz

./config.sh --url https://github.com/Fahim017803/devops-kb --token <YOUR_TOKEN>
# When prompted for a runner name, use: Fahim

# Run it in the background as a service
sudo ./svc.sh install
sudo ./svc.sh start
```

---

## 10. (Optional) Set up an Elastic IP so the address never changes

Without this, every stop/start gives you a **new public IP**, breaking any
bookmarked links or DNS records.

In AWS Console:
1. **EC2 → Network & Security → Elastic IPs → Allocate Elastic IP address**
2. Select the new IP → **Actions → Associate Elastic IP address**
3. Choose your instance → Associate

> Remember: an Elastic IP is free *only* while attached to a running instance.
> If you stop the instance and leave the IP allocated but unattached, it starts
> billing hourly. Release it if you're not actively using it.

---

## 11. (Optional) Re-issue SSL if you had a domain pointed here

If you previously had Let's Encrypt SSL set up for a domain:

```bash
sudo apt-get install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

This only works if your domain's DNS A record already points to the new IP.

---

## Quick reference — common commands after setup

```bash
# View logs
docker logs devops_kb_backend --tail 50
docker logs devops_kb_nginx --tail 50

# Restart everything after a code change
git pull
docker compose up -d --build

# Stop everything (e.g. to save cost when not in use)
docker compose down

# Check disk/memory if something seems broken
df -h
free -h
```

---

## What this guide does NOT cover

- Restoring actual article *content* — that lives in the MySQL database, not in
  Git. If the old EC2's database is gone, the `init.sql` seed articles will load,
  but anything written through the admin panel afterward needs to be re-entered.
- Domain DNS changes — if you have a custom domain, you'll need to update its
  A record to point to the new IP separately, in your domain registrar's settings.
