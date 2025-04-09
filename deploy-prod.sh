#!/bin/bash

# Backend deployment script
echo "[*] Building and starting backend services..."
docker compose -f prod.yml build --no-cache
docker compose -f prod.yml up -d

echo "[+] Backend done!"
