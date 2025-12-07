# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py runserver
RUN gunicorn --bind 0.0.0.0:8000 --workers 3 api.wsgi:application 
# CMD можно оставить как fallback, но в docker-compose.yml вы переопределяете его через `command`