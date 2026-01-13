#!/bin/bash

# Скрипт для создания superuser в Django с парсингом из .env файла

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Создание Django Superuser из .env файла ===${NC}"

# Функция для загрузки переменных из .env файла
load_env() {
    local env_file="${1:-.env}"
    
    if [ -f "$env_file" ]; then
        echo -e "${GREEN}Найден .env файл: $env_file${NC}"
        
        # Парсим .env файл, игнорируем комментарии и пустые строки
        while IFS='=' read -r key value || [[ -n "$key" ]]; do
            # Пропускаем комментарии и пустые строки
            if [[ $key =~ ^[[:space:]]*# ]] || [[ -z "$key" ]]; then
                continue
            fi
            
            # Удаляем кавычки и пробелы
            key=$(echo "$key" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
            value=$(echo "$value" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//; s/^["'\'']//; s/["'\'']$//')
            
            # Экспортируем переменную
            export "$key"="$value"
            
        done < <(grep -v '^#' "$env_file" | grep -v '^$')
        
        return 0
    else
        echo -e "${YELLOW}Файл .env не найден. Используются переменные окружения или значения по умолчанию.${NC}"
        return 1
    fi
}

# Функция для генерации случайного пароля
generate_password() {
    openssl rand -base64 16 | tr -d '/+=\n' | cut -c1-16
}

# Загружаем переменные из .env файла
load_env

# Устанавливаем значения по умолчанию или из .env
SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME:-${SUPERUSER_USERNAME:-admin}}"
SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-${SUPERUSER_EMAIL:-admin@example.com}}"
SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-${SUPERUSER_PASSWORD:-}}"

echo -e "\n${GREEN}Настройки superuser:${NC}"
echo "Имя пользователя: $SUPERUSER_USERNAME"
echo "Email: $SUPERUSER_EMAIL"
if [ "$GENERATED_PASSWORD" = true ]; then
    echo -e "Пароль: ${RED}$SUPERUSER_PASSWORD${NC} (сгенерирован автоматически)"
else
    echo "Пароль: [скрыт] (взят из .env файла)"
fi

# Проверяем, активировано ли виртуальное окружение
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Виртуальное окружение не активировано.${NC}"
    # Пробуем найти и активировать виртуальное окружение
    if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo -e "${GREEN}Активировано виртуальное окружение из venv/${NC}"
    elif [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        echo -e "${GREEN}Активировано виртуальное окружение из .venv/${NC}"
    fi
fi

# Проверяем, установлен ли Django
if ! python -c "import django" &> /dev/null; then
    echo -e "${RED}Django не установлен.${NC}"
    read -p "Установить Django? (y/n): " install_django
    if [ "$install_django" = "y" ]; then
        pip install django
    else
        echo -e "${RED}Прерывание выполнения.${NC}"
        exit 1
    fi
fi

# Проверяем наличие manage.py
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Файл manage.py не найден!${NC}"
    echo "Запустите скрипт из корневой директории Django проекта"
    exit 1
fi

# Создаем superuser
echo -e "\n${BLUE}Создаем superuser...${NC}"

# Пробуем создать через createsuperuser с --noinput
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
User.objects.filter(username='$SUPERUSER_USERNAME').exists() or \
User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')" | python manage.py shell

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Superuser успешно создан/обновлен!${NC}"
    
    # Выводим информацию
    echo -e "\n${BLUE}=== Информация для входа ===${NC}"
    echo "Имя пользователя: $SUPERUSER_USERNAME"
    echo "Email: $SUPERUSER_EMAIL"
    if [ "$GENERATED_PASSWORD" = true ]; then
        echo "Пароль: $SUPERUSER_PASSWORD"
        
        # Предлагаем обновить .env файл
        echo -e "\n${YELLOW}Хотите обновить .env файл с новым паролем?${NC}"
        read -p "(y/n): " update_env
        
        if [ "$update_env" = "y" ]; then
            # Обновляем или добавляем переменную в .env
            if grep -q "DJANGO_SUPERUSER_PASSWORD=" .env 2>/dev/null; then
                sed -i "s|^DJANGO_SUPERUSER_PASSWORD=.*|DJANGO_SUPERUSER_PASSWORD=$SUPERUSER_PASSWORD|" .env
            else
                echo "DJANGO_SUPERUSER_PASSWORD=$SUPERUSER_PASSWORD" >> .env
            fi
            echo -e "${GREEN}✓ .env файл обновлен${NC}"
        fi
    fi
    
    # Сохраняем данные в отдельный файл для безопасности
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    CREDS_FILE="superuser_creds_$TIMESTAMP.txt"
    
    cat > "$CREDS_FILE" << EOF
=== Django Superuser Credentials ===
Created: $(date)
Project: $(basename "$(pwd)")
Username: $SUPERUSER_USERNAME
Email: $SUPERUSER_EMAIL
Password: $SUPERUSER_PASSWORD
EOF
    
    chmod 600 "$CREDS_FILE"
    echo -e "${GREEN}✓ Данные сохранены в $CREDS_FILE${NC}"
    
else
    echo -e "${RED}✗ Ошибка при создании superuser${NC}"
    exit 1
fi