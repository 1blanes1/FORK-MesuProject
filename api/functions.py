import json
import asyncio
import os
import uuid

def generate_id():
    return str(uuid.uuid4())

import json
import os

def add_item_to_json(new_item, filename='news.json'):
    """
    Добавляет словарь new_item в JSON-файл, содержащий список словарей.
    
    :param new_item: словарь для добавления (например, {"title": "...", "desc": "...", "img_path": "..."})
    :param filename: путь к JSON-файлу (по умолчанию 'news.json')
    """
    # Если файл существует — загружаем данные, иначе создаём пустой список
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # Убеждаемся, что данные — это список
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                # Если файл повреждён — начинаем с пустого списка
                data = []
    else:
        data = []

    # Добавляем новый элемент
    data.append(new_item)

    # Сохраняем обратно в файл
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def get_item_by_id(target_id):
    try:
        with open("news.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Предполагается, что data — это список словарей
        for item in data:
            if item.get('id') == target_id:
                return item
        
        return None  # не найдено
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

import json

def read_json(file_path):
    """
    Читает JSON-файл и возвращает его содержимое как Python-объект.
    
    :param file_path: путь к файлу (например, 'data.json')
    :return: данные из файла (dict, list и т.д.) или None при ошибке
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка: файл {file_path} содержит некорректный JSON")
        return None
def delete_from_json_file(filepath, value):
    """
    Удаляет из JSON-файла все элементы, у которых field == value.

    :param filepath: путь к JSON-файлу (должен содержать список объектов)
    :param field: имя поля, по которому искать (например, 'title')
    :param value: значение, которое должно совпасть
    """
    field = "title"
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл {filepath} не найден")

    # Чтение данных
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Некорректный JSON в файле {filepath}: {e}")

    if not isinstance(data, list):
        raise ValueError("JSON-файл должен содержать список объектов")

    # Фильтрация: оставляем только те элементы, где поле НЕ равно value
    filtered_data = [item for item in data if item.get(field) != value]

    # Запись обратно в файл
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)

    print(f"Удалено {len(data) - len(filtered_data)} записей с {field} = {value!r}")
    pass