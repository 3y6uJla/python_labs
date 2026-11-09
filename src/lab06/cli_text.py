import argparse
import sys
from pathlib import Path

from src.lib.text import normalize, tokenize, count_freq, top_n
from src.lab04.io_txt_csv import read_text


def check_input(path: str) -> Path:
    """Функция проверяет, что входной файл существует

    Аргументы:
        path: путь к файлу

    Вывод:
        Путь к файлу в виде Path

    Ошибки:
        FileNotFoundError: если файла нет
        IsADirectoryError: если по пути лежит папка, а не файл
    """

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f'файл не найден: {path}')
    if path.is_dir():
        raise IsADirectoryError(f'{path} - это папка, а не файл')
    return path


def cat(path: str, number: bool) -> None:
    """Функция выводит содержимое файла построчно

    Аргументы:
        path: путь к файлу
        number: True - перед каждой строкой выводится ее номер

    Вывод:
        Ничего не возвращает, печатает строки файла

    Ошибки:
        FileNotFoundError: если файла нет
        IsADirectoryError: если указана папка
        UnicodeDecodeError: если файл не читается в utf-8
    """

    file = check_input(path)
    with open(file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, start=1):
            line = line.rstrip('\n')
            if number:
                print(f'{i:>4}  {line}')
            else:
                print(line)


def stats(path: str, top: int) -> None:
    """Функция выводит статистику слов в текстовом файле

    Аргументы:
        path: путь к текстовому файлу
        top: сколько самых частых слов вывести

    Вывод:
        Ничего не возвращает, печатает количество слов и топ слов по частоте

    Ошибки:
        FileNotFoundError: если файла нет
        IsADirectoryError: если указана папка
        UnicodeDecodeError: если файл не читается в utf-8
    """

    file = check_input(path)
    text = read_text(file)
    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)

    print(f'Всего слов: {len(tokens)}')
    print(f'Уникальных слов: {len(freq)}')

    if len(tokens) == 0:
        print('В файле нет слов')
        return

    print(f'Топ-{top}:')
    for word, count in top_n(freq, top):
        print(f'{word:<15}{count:>4}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Текстовые утилиты: вывод файла и частоты слов')
    subparsers = parser.add_subparsers(dest='command', required=True, title='подкоманды')

    cat_parser = subparsers.add_parser('cat', help='вывести содержимое файла построчно',
                                       description='Выводит содержимое файла построчно')
    cat_parser.add_argument('--input', required=True, help='путь к файлу')
    cat_parser.add_argument('-n', action='store_true', help='нумеровать строки')

    stats_parser = subparsers.add_parser('stats', help='частоты слов в тексте',
                                         description='Считает частоты слов в текстовом файле')
    stats_parser.add_argument('--input', required=True, help='путь к текстовому файлу')
    stats_parser.add_argument('--top', type=int, default=5,
                              help='сколько самых частых слов вывести (по умолчанию 5)')

    args = parser.parse_args()

    if args.command == 'stats' and args.top <= 0:
        stats_parser.error('--top должен быть больше 0')

    try:
        if args.command == 'cat':
            cat(args.input, args.n)
        elif args.command == 'stats':
            stats(args.input, args.top)
    except (FileNotFoundError, IsADirectoryError) as e:
        print(f'Ошибка: {e}', file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f'Ошибка: файл {args.input} не является текстовым файлом в кодировке utf-8',
              file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
