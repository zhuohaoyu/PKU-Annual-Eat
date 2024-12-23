# Build stage for Vue frontend
FROM dockerpull.org/library/node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json .
RUN npm config set registry https://registry.npmmirror.com
RUN npm install
COPY frontend/postcss.config.cjs .
COPY frontend/tailwind.config.cjs .
COPY frontend/src ./src
COPY frontend/index.html .
COPY frontend/vite.config.js .
RUN npm run build

# Final stage
FROM dockerpull.org/library/python:3.9-slim
WORKDIR /app
# Setup backend
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Install system dependencies for matplotlib
RUN apt-get update && \
    apt-get install -y \
    debian-keyring \
    debian-archive-keyring \
    apt-transport-https \
    curl \
    python3-tk \
    libfreetype6-dev \
    libpng-dev \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && apt-get update \
    && apt-get install -y caddy \
    && rm -rf /var/lib/apt/lists/*

# Create directory for frontend files
RUN mkdir -p /app/frontend/dist

# Copy frontend build
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist



COPY backend /app/backend
COPY Caddyfile /etc/caddy/Caddyfile
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 80

CMD ["/app/start.sh"] 