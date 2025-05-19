
# 🚀 ClassX Docker Setup Guide (Linux - Ubuntu)

This guide provides detailed instructions for setting up and running the ClassX application using Docker Compose on an **Ubuntu Linux** server. It includes prerequisites installation, environment configuration, Docker build steps, and GitHub/Docker authentication.

---

## ✅ Tested On

This setup has been tested with the following versions:

```bash
Git:              2.34.1
Docker:           28.1.1, build 4eba377
Docker Compose:   v2.35.1
```

---

## 1. Install Prerequisites

```bash
sudo apt update
sudo apt install -y git docker.io docker-compose-plugin make
```

Enable and start Docker:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Verify Docker is running:

```bash
sudo systemctl status docker
```

Verify tool installations:

```bash
git --version
docker --version
docker compose version
make --version
```

---

## 2. Authenticate with GitHub and Docker (If Needed)

### GitHub:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Docker (for GHCR/private registries):

```bash
docker login ghcr.io
```

> 🛑 **Note:** The application image is hosted in a **private GMU container registry**. Please contact the GMU ClassX team with your GitHub username to request access.

---

## 3. Clone the Repository

```bash
git clone https://github.com/stccenter/ClassX.git
cd ClassX
```

---

## 4. Set Up Environment File

```bash
cp .env.example .env
```

Then open `.env` and update all placeholder values:
- Secrets
- Domain/IPs
- OAuth config
- Logo file path (optional): `static/images/Logos/nasa-logo-png-nasa-logo.png`

---

## 5. Build Docker Images

```bash
make build
```

---

## 6. Start the Application

```bash
make up
```

---

## 7. Makefile Commands

| Command                  | Description                              |
|--------------------------|------------------------------------------|
| `make build`             | Build images from source Dockerfiles     |
| `make up`                | Start all services in detached mode      |
| `make down`              | Stop and remove containers + volumes     |
| `make reset`             | Fully stop, remove, and restart services |

---

## 8. Access the Application

- Keycloak Admin Console: `http://<your-domain>/keycloak`
- ClassX Frontend: `http://<your-domain>/`

---

