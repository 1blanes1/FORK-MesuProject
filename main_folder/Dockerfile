# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD можно оставить как fallback, но в docker-compose.yml вы переопределяете его через `command`