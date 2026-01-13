#!/bin/bash

DB_FILE="db.sqlite3"

# Проверяем, существует ли файл БД
if [ ! -f "$DB_FILE" ]; then
    echo "📁 Файл базы данных '$DB_FILE' не найден. Создаём пустой..."
    touch "$DB_FILE"
    chmod 666 "$DB_FILE"
    echo "✅ База данных создана: $DB_FILE"
else
    echo "✅ Файл базы данных уже существует: $DB_FILE"
fi

# Запуск Docker Compose
echo "🚀 Запуск сервисов через docker-compose..."
docker-compose up --build -d