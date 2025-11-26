
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

Пример выполнения
