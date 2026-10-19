import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.text import normalize, tokenize, count_freq, top_n
from lab04.io_txt_csv import read_text, write_csv

TOP_COUNT = 5


def load_text(path: str, encoding: str) -> str:
    """Функция читает файл, а при ошибке сообщает о ней и завершает программу

    Аргументы:
        path: путь к файлу
        encoding: кодировка файла

    Вывод:
        Содержимое файла одной строкой
    """

    try:
        return read_text(path, encoding=encoding)
    except FileNotFoundError:
        print(f'Ошибка: файл не найден: {path}', file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f'Ошибка: файл {path} не читается в кодировке {encoding}, '
              f'попробуйте --encoding cp1251', file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description='Отчёт по частотам слов в текстовом файле')
    parser.add_argument('--in', dest='input', default='data/lab04/input.txt',
                        help='входной файл')
    parser.add_argument('--out', default='data/lab04/report.csv',
                        help='файл отчёта')
    parser.add_argument('--encoding', default='utf-8',
                        help='кодировка входного файла')
    args = parser.parse_args()

    text = load_text(args.input, args.encoding)
    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    rows = top_n(freq, len(freq))

    write_csv(rows, args.out, header=('word', 'count'))

    print(f'Всего слов: {len(tokens)}')
    print(f'Уникальных слов: {len(freq)}')
    print(f'Топ-{TOP_COUNT}:')
    for word, count in top_n(freq, TOP_COUNT):
        print(f'{word}:{count}')


if __name__ == '__main__':
    main()
