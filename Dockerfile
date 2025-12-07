# Dockerfile
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . ..

# Открываем порт (для документации — Railway сам управляет портом)
EXPOSE $PORT

# Собираем статику и запускаем приложение при старте
CMD python manage.py collectstatic --noinput && \
    gunicorn --bind 0.0.0.0:$PORT json_api.wsgi:application