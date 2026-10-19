import csv
from pathlib import Path


def read_text(path: str | Path, encoding: str = 'utf-8') -> str:
    """Функция читает текстовый файл целиком и возвращает его содержимое

    Аргументы:
        path: путь к файлу (строка или Path)
        encoding: кодировка файла, по умолчанию 'utf-8'.
            Если файл сохранён в другой кодировке, её можно передать явно,
            например: read_text('data/lab04/input.txt', encoding='cp1251')

    Вывод:
        Содержимое файла одной строкой (для пустого файла - пустая строка '')

    Ошибки:
        FileNotFoundError: если файла нет
        UnicodeDecodeError: если файл не читается в указанной кодировке
    """

    with open(path, 'r', encoding=encoding) as f:
        return f.read()


def write_csv(rows: list[tuple | list], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    """Функция создаёт (или перезаписывает) CSV-файл с разделителем ','

    Аргументы:
        rows: список строк таблицы, каждая строка - кортеж или список
        path: путь к CSV-файлу
        header: заголовок таблицы, записывается первой строкой (если передан)

    Вывод:
        Ничего не возвращает. Если rows пустой и header=None - создаётся пустой файл,
        если rows пустой и header передан - в файле будет только заголовок

    Ошибки:
        ValueError: если строки в rows разной длины
    """

    for row in rows:
        if len(row) != len(rows[0]):
            raise ValueError(f'write_csv: строка {row} имеет длину {len(row)}, '
                             f'а первая строка - {len(rows[0])}')

    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if header is not None:
            writer.writerow(header)
        writer.writerows(rows)


if __name__ == '__main__':
    text = read_text('data/lab04/input.txt')
    print(f'read_text("data/lab04/input.txt") -> {text!r}')

    empty = read_text('data/lab04/empty.txt')
    print(f'read_text("data/lab04/empty.txt") -> {empty!r}')

    write_csv([('word', 'count'), ('test', 3)], 'data/lab04/check.csv')
    print('write_csv([("word", "count"), ("test", 3)], "data/lab04/check.csv") -> создан файл')

    write_csv([], 'data/lab04/check_header.csv', header=('a', 'b'))
    print('write_csv([], "data/lab04/check_header.csv", header=("a", "b")) -> только заголовок')

    try:
        write_csv([('a', 1), ('b',)], 'data/lab04/check_bad.csv')
    except ValueError as e:
        print(f'write_csv([("a", 1), ("b",)], ...) -> ValueError: {e}')
