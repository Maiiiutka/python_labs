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