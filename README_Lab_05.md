# ЛР5 — JSON и конвертации (JSON↔CSV, CSV→XLSX): Техническое задание

> **Цель:** Разобраться с форматом JSON, сериализацией/десериализацией и табличными конвертациями.  
> **Связь:** продолжение ЛР4 (работа с файлами) и подготовка базы для ЛР6 (CLI-конвертеры) и ЛР7 (тестирование).

---

## Результат ЛР
- Модуль `src/lab05/json_csv.py` с чистыми функциями:  
  - `json_to_csv(json_path, csv_path)`  
  - `csv_to_json(csv_path, json_path)`  
  (без вывода в stdout, только работа с файлами; валидация ошибок).

- Модуль `src/lab05/cvs_xlsx.py` с функцией  
  - `csv_to_xlsx(csv_path, xlsx_path)`  
  (через **openpyxl** или **xlsxwriter**, авто-ширина колонок).

- Примеры данных в `data/samples/` и артефакты конвертаций в `data/out/`:
  - `people.json` ⇄ `people_from_json.csv`
  - `people.csv` ⇄ `people_from_csv.json`
  - `people.xlsx` (из любого CSV)

- `README.md` с командами запуска, описанием форматов, допущений и скриншотами проверки XLSX.

- `requirements.txt` с одной зависимостью (**openpyxl** или **xlsxwriter**).  
  Всё остальное — стандартная библиотека (`json`, `csv`, `pathlib`).  
  Python **3.хх+**.

---
## Структура репозитория

```
python_labs/
├─ README.md                        #Общий отчет
├─ requirements.txt                # openpyxl или xlsxwriter, по выбору
├─ src/                             # здесь — все скрипты по заданиям
|  ├─ lib/                          # Переиспользуемые модули - хранить здесь
|  |  └── io_helpers.py             # Например чтение файлов из ЛР4
|  ├─ lab01
|  ........
|  ├─ lab04  
|  ├─ lab05/
|  |    ├── json_csv.py             # JSON↔CSV
│  |    ├── csv_xlsx.py             # CSV→XLSX
│  |    └── __init__.py
|  ........
|  └─ lab10
├─ data/
|   ├── samples/
│   │   ├── people.json             # пример входного JSON (список словарей)
│   │   ├── people.csv              # пример входного CSV
│   │   └── cities.csv              # дополнительный CSV для демонстрации
│   └── out/
│       ├── people_from_json.csv    # результат JSON→CSV
│       ├── people_from_csv.json    # результат CSV→JSON
│       └── people.xlsx             # результат CSV→XLSX

└─ images/                          # сюда — скриншоты работы программ
   ├─ lab01
   ........
   └─ lab10
```
---

## Теоретическая часть

### Что такое JSON
**JSON (JavaScript Object Notation)** — текстовый формат для обмена структурированными данными.  
Хранит объекты и списки, используется для сериализации и API.  

**Пример:**
```json
[
  {"name": "Alice", "age": 22},
  {"name": "Bob", "age": 25}
]
```

Python-модуль `json`:
- `json.load(f)` — загрузить из файла;
- `json.dump(obj, f, ensure_ascii=False, indent=2)` — записать в файл;
- `json.loads(s)` / `json.dumps(obj)` — работа со строками.

---

### Что такое CSV
**CSV (Comma-Separated Values)** — табличный текстовый формат, где значения разделены запятыми или `;`.

**Пример:**
```csv
name,age,city
Alice,22,SPB
Bob,25,Moscow
```

Python-модуль `csv`:
- `csv.DictReader(f)` — читает CSV как список словарей;
- `csv.DictWriter(f, fieldnames=...)` — записывает список словарей;
- `csv.Sniffer()` — автоопределение разделителя.

---

### JSON ↔ CSV ↔ XLSX
- JSON хранит **объекты** и **списки**.  
- CSV — **таблицы** (строки и колонки).  
- XLSX — **формат Excel**.  

Конвертация:
- JSON → CSV: объединение ключей → столбцы.  
- CSV → JSON: каждая строка → словарь.  
- CSV → XLSX: перенос строк в лист Excel, установка ширины колонок.

---
## ЗАДАНИЕ

### Задание A — JSON ↔ CSV
Реализовать модуль `src/lab05/json_csv.py` с функциями:
```python
def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Преобразует JSON-файл в CSV.
    Поддерживает список словарей [{...}, {...}], заполняет отсутствующие поля пустыми строками.
    Кодировка UTF-8. Порядок колонок — как в первом объекте или алфавитный (указать в README).
    """
def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Преобразует CSV в JSON (список словарей).
    Заголовок обязателен, значения сохраняются как строки.
    json.dump(..., ensure_ascii=False, indent=2)
    """
```

Code

```
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

```

Screen

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8ea707c7-5a01-4637-a2fb-cc08fff60ffb" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/4e60b446-2ff1-4a40-8042-72d78f2b0cf6" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/74d7839e-2e31-4242-a197-a3d82fc4d49d" />

#### **Требования**:
 - Проверка ошибок: 
    - неверный тип файла, пустой JSON или CSV → `ValueError`.
    - осутствующий файл → `FileNotFoundError`
 - Не использовать внешние пакеты (только json, csv, pathlib).
 - Все пути относительные.
 - Кодировка — строго UTF-8.

### Задание B — CSV → XLSX
Реализовать модуль `src/lab05/csv_xlsx.py`:
```python
def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """
    Конвертирует CSV в XLSX.
    Использовать openpyxl ИЛИ xlsxwriter.
    Первая строка CSV — заголовок.
    Лист называется "Sheet1".
    Колонки — автоширина по длине текста (не менее 8 символов).
    """
```

Code

```

import csv
from pathlib import Path
from openpyxl import Workbook

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """
    Конвертирует CSV в XLSX.
    
    Args:
        csv_path: Путь к исходному CSV файлу
        xlsx_path: Путь для сохранения XLSX файла
        
    Raises:
        FileNotFoundError: Если исходный файл не существует
        ValueError: Если CSV пустой или отсутствует заголовок
    """
    
    # Создание Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    # Чтение CSV
    with open(csv_path, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            ws.append(row)
    
    # Сохранение
    Path(xlsx_path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(xlsx_path)


if __name__ == "__main__":
    # Тестирование функции
    try:
        csv_to_xlsx("./data/Lab05/samples/people.csv", "./data/Lab05/out/people.xlsx")
        print("CSV -> XLSX успешно")
        
        # Дополнительный пример
        csv_to_xlsx("./data/Lab05/samples/cities.csv", "./data/Lab05/out/cities.xlsx")
        print("CSV -> XLSX (cities) успешно")
        
    except Exception as e:
        print(f"Ошибка: {e}")

```

Screen

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a28af710-63fa-4223-b382-49ec11116975" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d549cd3c-42fd-4525-9035-880e868dc427" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3da5270a-4607-4d8f-9129-7cebf6f67363" />

#### **Требования**:
 - Проверка ошибок: 
    - неверный тип файла, пустой JSON или CSV → `ValueError`.
    - осутствующий файл → `FileNotFoundError`
 - Не использовать внешние пакеты.
 - Все пути относительные.
 - Кодировка — строго UTF-8.
 - Результат — открываемый XLSX с корректной структурой таблицы.
---

## Примеры кода

### Пример 1. JSON чтение и запись
```python
import json
from pathlib import Path

data = [{"name": "Alice", "age": 22}, {"name": "Bob", "age": 25}]
path = Path("data/out/people.json")

with path.open("w", encoding="utf-8") as f:
    """ json.dump """

with path.open(encoding="utf-8") as f:
    """ json.load """
```

### Пример 2. Работа с CSV
```python
import csv

rows = [
    {"name": "Alice", "age": "22", "city": "SPB"},
    {"name": "Bob", "age": "25", "city": "Moscow"}
]

with open("data/out/people.csv", "w", newline="", encoding="utf-8") as f:
    """
        csv.DictWriter
    """

with open("data/out/people.csv", encoding="utf-8") as f:
    """
        csv.DictReader(f)
    """
```

### Пример 3. CSV → XLSX через openpyxl
```python
from openpyxl import Workbook
import csv

wb = Workbook()
ws = wb.active
ws.title = "Sheet1"

with open("data/samples/people.csv", encoding="utf-8") as f:
    """
        ws.append for row in csv.reader(f)
        
        wb.save("data/out/people.xlsx")
    """
```

### Пример 4. JSON → CSV
```python
import json, csv

with open("data/samples/people.json", encoding="utf-8") as jf:
    """ json.load """

with open("data/out/people_from_json.csv", "w", newline="", encoding="utf-8") as cf:
    """
        csv.DictReader(f)
    """
```

---

## Проверка и валидация
- Пустой JSON → `ValueError("Пустой JSON или неподдерживаемая структура")`  
- Список с не-словарами → `ValueError`  
- CSV без заголовка или пустой → `ValueError`  
- CSV отсутствует → ошибка при открытии.  
- Проверка: количество записей совпадает до и после конвертации.

---

## Набор данных и примеры
Для вашго удобства подготовлены мини-наборы:
- `data/samples/people.json` — список объектов одинаковой формы 
- `data/samples/people.csv` — CSV с теми же данными (для проверки обратимого преобразования).
- `data/samples/cities.csv` — CSV с 2–3 колонками для демонстрации CSV→XLSX.

От вас также требуется подготовить по 1 примеру файлов для каждого сценария.

**Сценарии демонстрации (описываются в README):**
1. JSON→CSV → проверка заголовка и количества строк.
2. CSV→JSON → сравнение ключей и количества объектов.
3. CSV→XLSX → открываем файл в Excel/LibreOffice, проверяем лист и ширины колонок.


## Что сдавать
1. Код в `src/lab05/*`.
