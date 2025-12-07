# Dockerfile
FROM python:3.11-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Собираем статику (если нужно)
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Запуск через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "json_api.wsgi:application"]