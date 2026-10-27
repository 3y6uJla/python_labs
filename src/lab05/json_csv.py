import csv
import json
from pathlib import Path


def check_file(path: str | Path, suffix: str) -> Path:
    """Функция проверяет входной файл перед чтением

    Аргументы:
        path: путь к файлу
        suffix: ожидаемое расширение, например '.json' или '.csv'

    Вывод:
        Путь к файлу в виде Path

    Ошибки:
        ValueError: если у файла другое расширение
        FileNotFoundError: если файла нет
    """

    path = Path(path)
    if path.suffix.lower() != suffix:
        raise ValueError(f'Неверный тип файла: {path.name}, ожидается {suffix}')
    if not path.is_file():
        raise FileNotFoundError(f'Файл не найден: {path}')
    return path


def check_out_file(path: str | Path, suffix: str) -> Path:
    """Функция проверяет расширение выходного файла и создаёт папку для него

    Аргументы:
        path: путь к выходному файлу
        suffix: ожидаемое расширение

    Вывод:
        Путь к файлу в виде Path

    Ошибки:
        ValueError: если у файла другое расширение
    """

    path = Path(path)
    if path.suffix.lower() != suffix:
        raise ValueError(f'Неверный тип файла: {path.name}, ожидается {suffix}')
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def json_to_csv(json_path: str, csv_path: str) -> None:
    """Функция преобразует JSON-файл в CSV

    JSON должен быть списком словарей [{...}, {...}]. Порядок колонок - как в первом
    объекте. Если у объекта нет какого-то поля, оно заполняется пустой строкой.

    Аргументы:
        json_path: путь к входному JSON-файлу
        csv_path: путь к выходному CSV-файлу

    Вывод:
        Ничего не возвращает, создаёт (или перезаписывает) CSV-файл в UTF-8

    Ошибки:
        FileNotFoundError: если JSON-файла нет
        ValueError: неверный тип файла, пустой или битый JSON, не список или в списке
            есть не словари, у объекта есть поле, которого нет в первом объекте,
            в значении лежит список или словарь (в одну ячейку CSV не влезает)
    """

    json_file = check_file(json_path, '.json')
    csv_file = check_out_file(csv_path, '.csv')

    with open(json_file, 'r', encoding='utf-8') as f:
        text = f.read()

    if text.strip() == '':
        raise ValueError('Пустой JSON или неподдерживаемая структура')

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f'Битый JSON в файле {json_file.name}: {e.msg}, строка {e.lineno}')

    if not isinstance(data, list) or len(data) == 0:
        raise ValueError('Пустой JSON или неподдерживаемая структура')

    for item in data:
        if not isinstance(item, dict):
            raise ValueError(f'В JSON есть элемент, который не является словарём: {item!r}')

    fieldnames = list(data[0].keys())
    if len(fieldnames) == 0:
        raise ValueError('Первый объект в JSON пустой, колонок нет')

    for i, item in enumerate(data, start=1):
        for key, value in item.items():
            if key not in fieldnames:
                raise ValueError(f'В объекте {i} есть поле "{key}", которого нет в первом объекте')
            if isinstance(value, (list, dict)):
                raise ValueError(f'В объекте {i} в поле "{key}" лежит список или словарь, '
                                 f'а в ячейку CSV помещается только одно значение')

    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
        writer.writeheader()
        writer.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    """Функция преобразует CSV в JSON (список словарей)

    Первая строка CSV - заголовок, каждая следующая строка становится словарём.
    Все значения сохраняются как строки.

    Аргументы:
        csv_path: путь к входному CSV-файлу
        json_path: путь к выходному JSON-файлу

    Вывод:
        Ничего не возвращает, создаёт (или перезаписывает) JSON-файл в UTF-8

    Ошибки:
        FileNotFoundError: если CSV-файла нет
        ValueError: неверный тип файла, пустой CSV, нет заголовка или нет строк с данными,
            в строке больше значений, чем колонок в заголовке
    """

    csv_file = check_file(csv_path, '.csv')
    json_file = check_out_file(json_path, '.json')

    with open(csv_file, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, restval='')
        header = reader.fieldnames

        if not header:
            raise ValueError('Пустой CSV или нет заголовка')
        for name in header:
            if name.strip() == '':
                raise ValueError('В заголовке CSV есть пустое название колонки')
        if len(set(header)) != len(header):
            raise ValueError('В заголовке CSV есть повторяющиеся колонки')

        rows = []
        for row in reader:
            if None in row:
                raise ValueError(f'В строке {reader.line_num} больше значений, чем колонок')
            rows.append(row)

    if len(rows) == 0:
        raise ValueError('В CSV нет строк с данными, только заголовок')

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def main() -> None:
    json_to_csv('data/samples/people.json', 'data/out/people_from_json.csv')
    with open('data/samples/people.json', encoding='utf-8') as f:
        people = json.load(f)
    with open('data/out/people_from_json.csv', encoding='utf-8', newline='') as f:
        csv_rows = list(csv.DictReader(f))
        header = list(csv_rows[0].keys())
    print('json_to_csv("data/samples/people.json", "data/out/people_from_json.csv")')
    print(f'  заголовок CSV: {header}')
    print(f'  объектов в JSON: {len(people)}, строк в CSV: {len(csv_rows)}')

    csv_to_json('data/samples/people.csv', 'data/out/people_from_csv.json')
    with open('data/samples/people.csv', encoding='utf-8', newline='') as f:
        csv_rows = list(csv.DictReader(f))
    with open('data/out/people_from_csv.json', encoding='utf-8') as f:
        people = json.load(f)
    print('\ncsv_to_json("data/samples/people.csv", "data/out/people_from_csv.json")')
    print(f'  ключи в JSON: {list(people[0].keys())}')
    print(f'  строк в CSV: {len(csv_rows)}, объектов в JSON: {len(people)}')

    json_to_csv('data/samples/students.json', 'data/out/students_from_json.csv')
    print('\njson_to_csv("data/samples/students.json", "data/out/students_from_json.csv")')
    with open('data/out/students_from_json.csv', encoding='utf-8', newline='') as f:
        print(f.read().strip())

    print('\nПроверка ошибок:')
    bad_calls = [
        ('json_to_csv', 'data/samples/empty.json'),
        ('json_to_csv', 'data/samples/broken.json'),
        ('json_to_csv', 'data/samples/not_dicts.json'),
        ('json_to_csv', 'data/samples/extra_keys.json'),
        ('json_to_csv', 'data/samples/people.csv'),
        ('json_to_csv', 'data/samples/nofile.json'),
        ('csv_to_json', 'data/samples/empty.csv'),
        ('csv_to_json', 'data/samples/only_header.csv'),
    ]
    for func_name, path in bad_calls:
        try:
            if func_name == 'json_to_csv':
                json_to_csv(path, 'data/out/bad.csv')
            else:
                csv_to_json(path, 'data/out/bad.json')
        except (ValueError, FileNotFoundError) as e:
            print(f'{func_name}("{path}", ...) -> {type(e).__name__}: {e}')


if __name__ == '__main__':
    main()
