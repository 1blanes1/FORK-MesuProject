# Dockerfile
FROM python:3.11-slim
RUN sed -i 's/deb.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list.d/debian.sources || \
    sed -i 's/deb.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем весь проект в /app
COPY . /app

# Устанавливаем рабочую директорию — корень проекта, где лежит manage.py
WORKDIR /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Собираем статику и запускаем Gunicorn
CMD python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    ./admin.sh && \
     gunicorn --bind 0.0.0.0:8000 json_api.wsgi:application