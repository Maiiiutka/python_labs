# ЛР6 — CLI‑утилиты с argparse (cat/grep‑lite + конвертеры): Техническое задание

> **Цель:** Научиться создавать консольные инструменты с аргументами командной строки, подкомандами и флагами.  
> **Связь:** продолжение ЛР5 (работа с JSON/CSV/XLSX) и подготовка к ЛР7 (тестирование).  
> Основная задача — обернуть существующие функции конвертации и анализа текста в CLI‑оболочки с помощью **argparse**.

---

## Результат ЛР

- Модуль `src/lab06/cli_text.py` с подкомандами:
  - `stats --input <txt> [--top 5]` — анализ частот слов в тексте (использовать функции из `lab03`);
  - `cat --input <path> [-n]` — вывод содержимого файла построчно (с нумерацией при `-n`).

- Модуль `src/lab06/cli_convert.py` с подкомандами:
  - `json2csv --in data/samples/people.json --out data/out/people.csv`  
  - `csv2json --in data/samples/people.csv --out data/out/people.json`  
  - `csv2xlsx --in data/samples/people.csv --out data/out/people.xlsx`  
  (использовать функции из `lab05`)

- Примеры запуска и скриншоты терминала — в `images/lab06/`.  
- `README.md` с кратким описанием всех подкоманд и параметров (`--help` и реальные примеры).  
- **Только стандартная библиотека** (`argparse`, `os`, `pathlib`, `sys` и ранее написанные функции).  
- Python **3.хх+**.

---
```
python_labs/
├─ README.md                       #Общий отчет
├─ src/                            # здесь — все скрипты по заданиям
|  ├─ lib/                         # Переиспользуемые модули - хранить здесь
|  |  └── io_helpers.py            
|  ├─ lab01
|  ........
|  ├─ lab05  
|  ├─ lab06/                       # Реализация кода
│  |   ├─ cli_text.py              
│  |   ├─ cli_convert.py
│  |   └─ __init__.py
|  ........
|  └─ lab10
├─ data/
|   ├── samples
│   └── out
|
└─ images/                         # сюда — скриншоты работы программ
   ├─ lab01
   ........
   └─ lab10
```
---

## Теоретическая часть

### Что такое CLI‑утилита
**CLI (Command Line Interface)** — интерфейс взаимодействия через консоль.  
CLI‑программы позволяют вызывать функции программы через команды и флаги, например:
```bash
python -m src.lab06.cli_convert json2csv --in data/samples/people.json --out data/out/people.csv
```

### Что такое argparse
Модуль **argparse** — стандартный инструмент Python для парсинга аргументов командной строки.

**Основные понятия:**
- `ArgumentParser` — объект, описывающий интерфейс программы;
- `add_argument()` — добавление параметров (`--input`, `--output`, `-n`, и т.д.);
- `add_subparsers()` — создание подкоманд (`stats`, `cat`, `json2csv` и др.).

**Минимальный пример:**
```python
import argparse

parser = argparse.ArgumentParser(description="Пример CLI")
parser.add_argument("--name", required=True, help="Имя пользователя")
args = parser.parse_args()
print(f"Привет, {args.name}!")
```

**Результат запуска:**
```bash
$ python hello.py --name Alice
Привет, Alice!
```
---

## Примеры кода

### Пример 1. Подкоманды в одном CLI
```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="CLI‑утилиты лабораторной №6")
    subparsers = parser.add_subparsers(dest="command")

    # подкоманда cat
    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", required=True)
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")

    # подкоманда stats
    stats_parser = subparsers.add_parser("stats", help="Частоты слов")
    stats_parser.add_argument("--input", required=True)
    stats_parser.add_argument("--top", type=int, default=5)

    args = parser.parse_args()

    if args.command == "cat":
        """ Реализация команды cat """
    elif args.command == "stats":
        """ Реализация команды stats """
```

Code

```
import argparse
from pathlib import Path
import sys

# Импортируем функции из lab05 или другого модуля, если есть

def analyze_text(text, top=5):
    # Простая функция подсчёта слов
    from collections import Counter
    words = text.lower().split()
    counter = Counter(words)
    return counter.most_common(top)

def main():
    parser = argparse.ArgumentParser(description="CLI‑утилиты для анализа текста")
    subparsers = parser.add_subparsers(dest='command')

    # команда stats
    parser_stats = subparsers.add_parser('stats', help='Анализ частот слов')
    parser_stats.add_argument('--input', required=True, help='Путь к текстовому файлу')
    parser_stats.add_argument('--top', type=int, default=5, help='Количество топ‑слов для отображения')

    # команда cat
    parser_cat = subparsers.add_parser('cat', help='Вывести содержимое файла')
    parser_cat.add_argument('--input', required=True, help='Путь к файлу')
    parser_cat.add_argument('-n', action='store_true', help='Показать нумерацию строк')

    args = parser.parse_args()

    if args.command == 'stats':
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
            result = analyze_text(text, top=args.top)
            print("Топ слов:")
            for word, count in result:
                print(f"{word}: {count}")
        except FileNotFoundError:
            print(f"Файл не найден: {args.input}")
    elif args.command == 'cat':
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, start=1):
                    if args.n:
                        print(f"{i}\t{line.rstrip()}")
                    else:
                        print(line.rstrip())
        except FileNotFoundError:
            print(f"Файл не найден: {args.input}")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

---

### Пример 2. CLI‑конвертер
```python
import argparse
from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx

def main():
    parser = argparse.ArgumentParser(description="Конвертеры данных")
    sub = parser.add_subparsers(dest="cmd")

    p1 = sub.add_parser("json2csv")
    p1.add_argument("--in", dest="input", required=True)
    p1.add_argument("--out", dest="output", required=True)

    p2 = sub.add_parser("csv2json")
    p2.add_argument("--in", dest="input", required=True)
    p2.add_argument("--out", dest="output", required=True)

    p3 = sub.add_parser("csv2xlsx")
    p3.add_argument("--in", dest="input", required=True)
    p3.add_argument("--out", dest="output", required=True)

    args = parser.parse_args()

    """
        Вызываем код в зависимости от аргументов.
    """
```

Code

```
import sys
import os
import argparse

# Вставляем корень проекта, чтобы модули находились
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.Sem1.Lab05 import csv_xlsx
from src.Sem1.Lab05 import json_csv

def main():
    parser = argparse.ArgumentParser(description="Конвертация данных")
    subparsers = parser.add_subparsers(dest='command')

    # json2csv
    parser_json2csv = subparsers.add_parser('json2csv')
    parser_json2csv.add_argument('--in', dest='input', required=True)
    parser_json2csv.add_argument('--out', dest='output', required=True)

    # csv2json
    parser_csv2json = subparsers.add_parser('csv2json')
    parser_csv2json.add_argument('--in', dest='input', required=True)
    parser_csv2json.add_argument('--out', dest='output', required=True)

    # csv2xlsx
    parser_csv2xlsx = subparsers.add_parser('csv2xlsx')
    parser_csv2xlsx.add_argument('--in', dest='input', required=True)
    parser_csv2xlsx.add_argument('--out', dest='output', required=True)

    args = parser.parse_args()

    if args.command == 'json2csv':
        try:
            json_csv.json_to_csv(args.input, args.output)
            print(f"Конвертация {args.input} из JSON в CSV завершена.")
        except Exception as e:
            print(f"Ошибка: {e}")

    elif args.command == 'csv2json':
        try:
            json_csv.csv_to_json(args.input, args.output)
            print(f"Конвертация {args.input} из CSV в JSON завершена.")
        except Exception as e:
            print(f"Ошибка: {e}")

    elif args.command == 'csv2xlsx':
        try:
            csv_xlsx.csv_to_xlsx(args.input, args.output)
            print(f"Конвертация {args.input} из CSV в XLSX завершена.")
        except Exception as e:
            print(f"Ошибка: {e}")
    else:
        print("Неизвестная команда.")
        parser.print_help()

if __name__ == '__main__':
    main()
```

---

## Проверка и демонстрация

**Файлы для демонстрации:**
- Использовать данные из `data/samples/` из ЛР5.  
- Результаты сохраняются в `data/out/`.

**Сценарии проверки (описать в README):**
1. `cat --input data/samples/people.csv -n` → вывод строк с номерами.  
2. `stats --input data/samples/people.txt --top 5` → вывод топ‑слов.  
3. `json2csv`, `csv2json`, `csv2xlsx` — корректная конвертация без ошибок.  
4. Проверка `--help` для каждой подкоманды.

---

## Валидация и обработка ошибок
- Отсутствие входного файла → `FileNotFoundError`.  
- Неверные аргументы → вывод `parser.error(...)`.  
- Все сообщения — понятные, человекочитаемые.  
- Вывод справки (`--help`) должен работать без ошибок.  
- Код не должен зависеть от внешних библиотек.

---

## Что сдавать
1. Код в `src/lab06/*`  
2. Файлы демонстрации в `data/out/`  
3. `README.md` с командами запуска и примерами вывода (скриншоты) 
4. Скриншоты в `images/lab06/`

---
