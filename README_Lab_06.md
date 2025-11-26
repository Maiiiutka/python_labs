
### Пример 1. Подкоманды в одном CLI

```
import argparse
from collections import Counter
import os
import sys


def read_file(file_path):
    """Чтение файла с проверкой его существования"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден")
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()


def cat_command(input_file, number_lines=False):
    """Реализация команды cat с нумерацией строк"""
    lines = read_file(input_file)
    for i, line in enumerate(lines, 1):
        if number_lines:
            print(f"{i:6d}\t{line.rstrip()}")
        else:
            print(line.rstrip())


def stats_command(input_file, top_n=5):
    """Реализация команды stats с подсчетом частоты слов"""
    lines = read_file(input_file)
    words = []
    for line in lines:
        # Более аккуратная обработка слов - убираем пунктуацию
        line_words = line.strip().lower().split()
        cleaned_words = [word.strip('.,!?;:"()[]') for word in line_words]
        words.extend(cleaned_words)

    # Убираем пустые строки
    words = [word for word in words if word]

    counter = Counter(words)
    most_common = counter.most_common(top_n)

    print(f"Топ-{top_n} самых частых слов:")
    for i, (word, count) in enumerate(most_common, 1):
        print(f"{i:2d}. {word:<15} {count:>3} раз(а)")


def main():
    parser = argparse.ArgumentParser(
        description="CLI‑утилиты лабораторной №6",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
```

Примеры использования:

```
  python cli_text.py cat --input example.txt
  python cli_text.py cat --input example.txt -n
  python cli_text.py stats --input example.txt
  python cli_text.py stats --input example.txt --top 10
        """
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="доступные команды",
        metavar="команда"
    )

    # Подкоманда cat
    cat_parser = subparsers.add_parser("cat", help="вывести содержимое файла")
    cat_parser.add_argument("--input", required=True, help="путь к входному файлу")
    cat_parser.add_argument("-n", action="store_true", help="нумеровать строки")

    # Подкоманда stats
    stats_parser = subparsers.add_parser("stats", help="статистика частот слов")
    stats_parser.add_argument("--input", required=True, help="путь к входному файлу")
    stats_parser.add_argument("--top", type=int, default=5, help="количество топ-слов (по умолчанию: 5)")

    args = parser.parse_args()

    if not args.command:
        # Если команда не указана, показываем справку
        parser.print_help()
        return

    try:
        if args.command == "cat":
            cat_command(args.input, args.n)
        elif args.command == "stats":
            stats_command(args.input, args.top)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

#### Пояснение

Подкоманда cat: --input - обязательный аргумент, указывающий на входной файл. -n - опция, при указании которой нужно выводить номера строк.

Подкоманда stats: --input - обязательный аргумент, указывающий на входной файл. --top - опция, указывающая, сколько самых частых слов показывать (по умолчанию 5).

Реализация: Для cat: Прочитать файл и вывести его содержимое. Если задан флаг -n, то перед каждой строкой вывести ее номер (начиная с 1). Для stats: Прочитать файл, разбить текст на слова (разделители: пробелы, переносы строк и т.п.), подсчитать частоты слов, вывести top самых частых слов (по убыванию частоты). Если несколько слов имеют одинаковую частоту, то выводить их в лексикографическом порядке.

Примечание: в подкоманде stats слова следует считать в нижнем регистре, чтобы регистр не влиял на подсчет.


#### Пример вызова и вывода:


cat --input file.txt -n 1: первая строка 2: вторая строка

stats --input file.txt --top 3 слово1: 10 слово2: 5 слово3: 3

###### Дополнительно: обработать возможные ошибки (например, файл не найден). В случае ошибки вывести сообщение и завершить программу.

Или более подробно
Get-ChildItem "" 2) Создала файл cli_text.py @" import argparse from collections import Counter import os import sys

def read_file(file_path): if not os.path.exists(file_path): raise FileNotFoundError(f"Файл {file_path} не найден") with open(file_path, 'r', encoding='utf-8') as f: return f.readlines()

def cat_command(input_file, number_lines=False): lines = read_file(input_file) for i, line in enumerate(lines, 1): if number_lines: print(f"{i:6d}\t{line.rstrip()}") else: print(line.rstrip())

def stats_command(input_file, top_n=5): lines = read_file(input_file) words = [] for line in lines: line_words = line.strip().lower().split() cleaned_words = [word.strip('.,!?;:"()[]') for word in line_words] words.extend(cleaned_words)

```
words = [word for word in words if word]
counter = Counter(words)
most_common = counter.most_common(top_n)

print(f"Топ-{top_n} самых частых слов:")
```

for i, (word, count) in enumerate(most_common, 1):
    print(f"{i:2d}. {word:<15} {count:>3} раз(а)")
def main(): parser = argparse.ArgumentParser(description="CLI утилиты") subparsers = parser.add_subparsers(dest="command", required=True)

```
cat_parser = subparsers.add_parser("cat", help="вывести содержимое файла")
cat_parser.add_argument("--input", required=True)
cat_parser.add_argument("-n", action="store_true")

stats_parser = subparsers.add_parser("stats", help="статистика частот слов")
stats_parser.add_argument("--input", required=True)
stats_parser.add_argument("--top", type=int, default=5)

args = parser.parse_args()

try:
    if args.command == "cat":
        cat_command(args.input, args.n)
    elif args.command == "stats":
        stats_command(args.input, args.top)
except Exception as e:
    print(f"Ошибка: {e}")
```

if name == "main": main() "@ | Out-File -FilePath "cli_text.py" -Encoding UTF8 3) Создала файл example.txt @" hello world hello test this is a test file hello again world testing one two three "@ | Out-File -FilePath "example.txt" -Encoding UTF8 4) Проверила, что файлы созданы. ls 5) Запустила команды:

Проверила справку
python cli_text.py

Команда cat без нумерации
python cli_text.py cat --input example.txt

Команда cat с нумерацией
python cli_text.py cat --input example.txt -n

Команда stats
python cli_text.py stats --input example.txt

Команда stats с ограничением
python cli_text.py stats --input example.txt --top 3

#### Пример выполнения

Проверила справку
python cli_text.py

Команда cat без нумерации
python cli_text.py cat --input example.txt

Команда cat с нумерацией
python cli_text.py cat --input example.txt -n

Команда stats
python cli_text.py stats --input example.txt

Команда stats с ограничением
python cli_text.py stats --input example.txt --top 3

<img width="750" height="306" alt="image" src="https://github.com/user-attachments/assets/397d7e50-8c9d-44eb-8f2d-dd9f08d3d275" />
<img width="805" height="228" alt="image" src="https://github.com/user-attachments/assets/1ca272dd-d1fe-41f9-b9d2-0a7b488dd69f" />

### Пример 2. CLI‑конвертер
```
import argparse
import sys
import os
import json
import csv
from collections import Counter
import re


def read_file(filename):
    """Чтение файла с обработкой ошибок"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден: {os.path.abspath(filename)}")
        print(f"Текущая директория: {os.getcwd()}")
        print("Доступные файлы в текущей директории:")
        for item in os.listdir('.'):
            print(f"  - {item}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
        sys.exit(1)


def write_file(filename, content, mode='w'):
    """Запись файла с обработкой ошибок"""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, mode, encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Ошибка при записи файла {filename}: {e}")
        sys.exit(1)


def cat_command(input_file, number_lines):
    """Команда cat - вывод содержимого файла"""
    lines = read_file(input_file)
    for i, line in enumerate(lines, 1):
        if number_lines:
            print(f"{i:6d}\t{line.rstrip()}")
        else:
            print(line.rstrip())


def stats_command(input_file, top_n):
    """Команда stats - статистика частот слов"""
    if top_n <= 0:
        print("Ошибка: параметр --top должен быть положительным числом")
        sys.exit(1)

    lines = read_file(input_file)
    text = ' '.join(lines)

    # Разбивка на слова с игнорированием регистра
    words = re.findall(r'\b\w+\b', text.lower())

    if not words:
        print("Файл не содержит слов")
        return

    # Подсчет частот
    counter = Counter(words)

    # Вывод топ-N
    print(f"Топ-{top_n} самых частых слов:")
    for word, count in counter.most_common(top_n):
        print(f"{word}: {count}")


def json_to_csv(input_file, output_file):
    """Конвертация JSON в CSV"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not data:
            print("Предупреждение: JSON файл пуст")
            return

        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # Список словарей
            fieldnames = data[0].keys() if data else []
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"Успешно: {input_file} -> {output_file}")
        else:
            print("Ошибка: JSON должен содержать список словарей")
            sys.exit(1)

    except json.JSONDecodeError as e:
        print(f"Ошибка: Неверный формат JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при конвертации JSON в CSV: {e}")
        sys.exit(1)


def csv_to_json(input_file, output_file):
    """Конвертация CSV в JSON"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Успешно: {input_file} -> {output_file}")

    except csv.Error as e:
        print(f"Ошибка: Неверный формат CSV: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при конвертации CSV в JSON: {e}")
        sys.exit(1)


def csv_to_xlsx(input_file, output_file):
    """Конвертация CSV в XLSX (заглушка - требует внешней библиотеки)"""
    print("Ошибка: Конвертация CSV в XLSX требует установки внешней библиотеки (openpyxl или xlsxwriter)")
    print("Установите библиотеку: pip install openpyxl")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="CLI‑утилиты для работы с файлами и конвертации данных",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Простые примеры использования:
  python cli_convert.py cat --input "test_data/samples/people.csv" -n
  python cli_convert.py stats --input "test_data/samples/people.txt" --top 5
  python cli_convert.py json2csv --in "test_data/samples/data.json" --out "test_data/out/data.csv"
  python cli_convert.py csv2json --in "test_data/samples/people.csv" --out "test_data/out/people.json"
        """
    )

    subparsers = parser.add_subparsers(dest="command", title="доступные команды", help="выберите команду")

    # Подкоманда cat
    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", required=True, help="Входной файл")
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")

    # Подкоманда stats
    stats_parser = subparsers.add_parser("stats", help="Статистика частот слов")
    stats_parser.add_argument("--input", required=True, help="Входной файл")
    stats_parser.add_argument("--top", type=int, default=5, help="Количество топ-слов (по умолчанию: 5)")

    # Подкоманда json2csv
    json2csv_parser = subparsers.add_parser("json2csv", help="Конвертировать JSON в CSV")
    json2csv_parser.add_argument("--in", dest="input", required=True, help="Входной JSON файл")
    json2csv_parser.add_argument("--out", dest="output", required=True, help="Выходной CSV файл")

    # Подкоманда csv2json
    csv2json_parser = subparsers.add_parser("csv2json", help="Конвертировать CSV в JSON")
    csv2json_parser.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    csv2json_parser.add_argument("--out", dest="output", required=True, help="Выходной JSON файл")

    # Подкоманда csv2xlsx
    csv2xlsx_parser = subparsers.add_parser("csv2xlsx", help="Конвертировать CSV в XLSX (требует openpyxl)")
    csv2xlsx_parser.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    csv2xlsx_parser.add_argument("--out", dest="output", required=True, help="Выходной XLSX файл")

    args = parser.parse_args()

    # Если команда не указана, показать помощь
    if not args.command:
        parser.print_help()
        return

    # Выполнение команд
    if args.command == "cat":
        cat_command(args.input, args.n)
    elif args.command == "stats":
        stats_command(args.input, args.top)
    elif args.command == "json2csv":
        json_to_csv(args.input, args.output)
    elif args.command == "csv2json":
        csv_to_json(args.input, args.output)
    elif args.command == "csv2xlsx":
        csv_to_xlsx(args.input, args.output)


if __name__ == "__main__":
    main()
```

Пояснение
Создает файлы прямо в папке src/lab06/test_data/ (проще для отладки). Использует относительные пути без сложных конструкций ../../../. Выводит много информации при ошибках. Показывает список файлов в текущей директории при ошибке "файл не найден".

Запуск
Создала тестовые файлы
python test_data.py

import os
import json

```
def create_simple_test_data():
    """Создает тестовые файлы прямо в папке lab06 для простоты"""
    
    # Создаем папки прямо здесь
    os.makedirs("test_data/samples", exist_ok=True)
    os.makedirs("test_data/out", exist_ok=True)
    
    print("Создаем тестовые файлы в папке test_data/")
    
    # Создаем people.csv
    csv_content = """name,age,city
Иван,25,Москва
Мария,30,Санкт-Петербург
Петр,35,Казань
Анна,28,Новосибирск
Сергей,32,Екатеринбург"""
    
    with open("test_data/samples/people.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)
    print("Создан: test_data/samples/people.csv")
    
    # Создаем people.txt
    txt_content = """Это тестовый файл для демонстрации работы утилиты.
Файл содержит несколько строк текста на русском языке.
Мы будем анализировать частоты слов в этом тексте.
Текст текст текст - повторяющиеся слова должны быть найдены.
Это предложение содержит слова для статистического анализа."""
    
    with open("test_data/samples/people.txt", "w", encoding="utf-8") as f:
        f.write(txt_content)
    print("Создан: test_data/samples/people.txt")
    
    # Создаем data.json
    json_data = [
        {"name": "Иван", "age": 25, "city": "Москва"},
        {"name": "Мария", "age": 30, "city": "Санкт-Петербург"},
        {"name": "Петр", "age": 35, "city": "Казань"}
    ]
    
    with open("test_data/samples/data.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print("Создан: test_data/samples/data.json")
    
    print("\nТестовые файлы успешно созданы в папке test_data/")
    print("\nПримеры команд:")
    print('  python cli_convert.py cat --input "test_data/samples/people.csv" -n')
    print('  python cli_convert.py stats --input "test_data/samples/people.txt" --top 5')
    print('  python cli_convert.py json2csv --in "test_data/samples/data.json" --out "test_data/out/data.csv"')
    print('  python cli_convert.py csv2json --in "test_data/samples/people.csv" --out "test_data/out/people.json"')

if __name__ == "__main__":
    create_simple_test_data()
```

Запустила этот скрипт
python create_simple_test_data.py

Проверила команды
python cli_convert.py cat --input "test_data/samples/people.csv" -n python cli_convert.py stats --input "test_data/samples/people.txt" --top 5 python cli_convert.py json2csv --in "test_data/samples/data.json" --out "test_data/out/data.csv" python cli_convert.py csv2json --in "test_data/samples/people.csv" --out "test_data/out/people.json"

Пример выполнения:

<img width="646" height="160" alt="image" src="https://github.com/user-attachments/assets/1af785ef-7479-4882-92a5-96800189c246" />
<img width="1170" height="186" alt="image" src="https://github.com/user-attachments/assets/4105afcc-e221-40ef-ad59-53ab43694b07" />

### Вывод
Научилась создавать консольные инструменты с аргументами командной строки, подкомандами и флагами.
