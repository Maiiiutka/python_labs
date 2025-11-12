import csv
import json
from pathlib import Path
from typing import List, Dict, Any

def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Преобразует JSON-файл в CSV.
    Поддерживает список словарей [{...}, {...}], заполняет отсутствующие поля пустыми строками.
    Кодировка UTF-8. Порядок колонок — как в первом объекте или алфавитный (указать в README).
    """
    json_file = Path(json_path)
    if not json_file.exists():
        raise ValueError(f"Неверный путь к файлу.")
    
    if json_file.suffix != ".json":
        raise ValueError(f"Неверный тип файла: ожидается .json. Получен: {json_file.suffix}")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON: {e}")
    
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать список объектов")
    
    if len(data) == 0:
        raise ValueError("Файл JSON пуст")
    
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Все элементы файла JSON должны быть словорями")
    
    # Получаем все названия колонок
    header = set()
    for item in data:
        if isinstance(item, dict):
            header.update(item.keys())
    
    columns = sorted(list(header))
    
    # Пишем CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        
        for item in data:
            # Заполняем пустые места
            row = {}
            for col in columns:
                row[col] = item.get(col, '')
            writer.writerow(row)

def csv_to_json(csv_file, json_file):
    """
    Просто преобразуем CSV в JSON
    """
    data = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    # Сохраняем красивый JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Проверка работы
if __name__ == "__main__":
    try:
        json_to_csv("./data/Lab05/samples/people.json", "./data/Lab05/out/from_json.csv")
        print("JSON -> CSV готово!")
        
        csv_to_json("./data/Lab05/samples/people.csv", "./data/Lab05/out/from_csv.json")
        print("CSV -> JSON готово!")
        
    except Exception as e:
        print(f"Ошибка: {e}")