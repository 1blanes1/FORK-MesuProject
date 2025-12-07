# Используем официальный Python-образ
FROM python:3.11-slim

# Устанавливаем зависимости ОС (если нужны)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY main_folder/ .

# Собираем статику (если нужно)
RUN python manage.py collectstatic --noinput

# Запуск через gunicorn с использованием $PORT
# ⚠️ Обязательно в shell-форме, чтобы подставилась переменная
CMD gunicorn --bind 0.0.0.0:$PORT json_api.wsgi:application