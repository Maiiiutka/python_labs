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