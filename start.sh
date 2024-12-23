#!/bin/bash
set -e

# Start Flask backend
cd /app/backend
python app.py &

# Start Caddy in foreground
exec caddy run --config /etc/caddy/Caddyfile --adapter caddyfile 