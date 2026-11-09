import argparse
import sys

from src.lab05.json_csv import json_to_csv, csv_to_json


def main() -> None:
    parser = argparse.ArgumentParser(description='Конвертеры данных: JSON, CSV, XLSX')
    subparsers = parser.add_subparsers(dest='command', required=True, title='подкоманды')

    commands = [
        ('json2csv', 'JSON -> CSV', 'входной .json файл', 'выходной .csv файл'),
        ('csv2json', 'CSV -> JSON', 'входной .csv файл', 'выходной .json файл'),
        ('csv2xlsx', 'CSV -> XLSX', 'входной .csv файл', 'выходной .xlsx файл'),
    ]

    for name, help_text, in_help, out_help in commands:
        p = subparsers.add_parser(name, help=help_text, description=f'Конвертация {help_text}')
        p.add_argument('--in', dest='input', required=True, help=in_help)
        p.add_argument('--out', dest='output', required=True, help=out_help)

    args = parser.parse_args()

    try:
        if args.command == 'json2csv':
            json_to_csv(args.input, args.output)
        elif args.command == 'csv2json':
            csv_to_json(args.input, args.output)
        elif args.command == 'csv2xlsx':
            from src.lab05.csv_xlsx import csv_to_xlsx
            csv_to_xlsx(args.input, args.output)
    except FileNotFoundError as e:
        print(f'Ошибка: {e}', file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f'Ошибка: файл {args.input} не читается в кодировке utf-8', file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f'Ошибка: {e}', file=sys.stderr)
        sys.exit(1)

    print(f'Готово: {args.input} -> {args.output}')


if __name__ == '__main__':
    main()
