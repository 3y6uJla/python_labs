# Лабораторная работа 5


```bash
pip install -r requirements.txt
```

## Задание A - JSON и CSV `src/lab05/json_csv.py`

### 1. Вспомогательные функции проверки файлов

Обе функции конвертации сначала проверяют файлы. У входного файла проверяется расширение и то, что файл существует. У выходного файла проверяется расширение, а папка для него создается, если ее еще нет.

```python
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
```

### 2. Функция `json_to_csv`

Функция читает JSON-файл, который должен быть списком словарей, и записывает его в CSV через `csv.DictWriter`.

Порядок колонок как в первом объекте. Если в следующих объектах встречаются новые ключи, они добавляются в конец в порядке появления. Если у объекта нет какого-то поля, в CSV на этом месте записывается пустая строка (`restval=''`).

```python
def json_to_csv(json_path: str, csv_path: str) -> None:
    """Функция преобразует JSON-файл в CSV

    JSON должен быть списком словарей [{...}, {...}]. Порядок колонок - как в первом
    объекте, ключи, которых нет в первом объекте, добавляются в конец в порядке появления.
    Отсутствующие поля заполняются пустой строкой.

    Аргументы:
        json_path: путь к входному JSON-файлу
        csv_path: путь к выходному CSV-файлу

    Вывод:
        Ничего не возвращает, создаёт (или перезаписывает) CSV-файл в UTF-8

    Ошибки:
        FileNotFoundError: если JSON-файла нет
        ValueError: неверный тип файла, пустой или некорректный JSON,
            не список или в списке есть не словари
    """

    json_file = check_file(json_path, '.json')
    csv_file = check_out_file(csv_path, '.csv')

    with open(json_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f'Файл {json_file.name} не является корректным JSON')

    if not isinstance(data, list) or len(data) == 0:
        raise ValueError('Пустой JSON или неподдерживаемая структура')

    for item in data:
        if not isinstance(item, dict):
            raise ValueError(f'В JSON есть элемент, который не является словарём: {item!r}')

    fieldnames = []
    for item in data:
        for key in item:
            if key not in fieldnames:
                fieldnames.append(key)

    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
        writer.writeheader()
        writer.writerows(data)
```

### 3. Функция `csv_to_json`

Функция читает CSV через `csv.DictReader`, каждая строка превращается в словарь, где ключи это названия колонок из заголовка. Все значения сохраняются как строки, потому что CSV не хранит типы данных. Запись выполняется через `json.dump(..., ensure_ascii=False, indent=2)`, поэтому русские буквы в JSON остаются читаемыми.

```python
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
```

### 4. Обработка ошибок

| Ситуация | Ошибка |
|---|---|
| Файла нет | `FileNotFoundError` |
| Неверное расширение файла (например, `.csv` вместо `.json`) | `ValueError` |
| JSON не читается (синтаксическая ошибка) | `ValueError` |
| Пустой JSON `[]` или JSON не является списком | `ValueError("Пустой JSON или неподдерживаемая структура")` |
| В списке JSON есть элементы, которые не являются словарями | `ValueError` |
| Пустой CSV или CSV без заголовка | `ValueError` |
| В заголовке CSV пустая или повторяющаяся колонка | `ValueError` |
| В CSV только заголовок, без строк с данными | `ValueError` |
| В строке CSV больше значений, чем колонок | `ValueError` |

### 5. Проверка модуля

```python
if __name__ == '__main__':
    json_to_csv('data/samples/people.json', 'data/out/people_from_json.csv')
    with open('data/samples/people.json', encoding='utf-8') as f:
        people = json.load(f)
    with open('data/out/people_from_json.csv', encoding='utf-8') as f:
        csv_rows = list(csv.DictReader(f))
        header = list(csv_rows[0].keys())
    print('json_to_csv("data/samples/people.json", "data/out/people_from_json.csv")')
    print(f'  заголовок CSV: {header}')
    print(f'  объектов в JSON: {len(people)}, строк в CSV: {len(csv_rows)}')

    csv_to_json('data/samples/people.csv', 'data/out/people_from_csv.json')
    with open('data/samples/people.csv', encoding='utf-8') as f:
        csv_rows = list(csv.DictReader(f))
    with open('data/out/people_from_csv.json', encoding='utf-8') as f:
        people = json.load(f)
    print('\ncsv_to_json("data/samples/people.csv", "data/out/people_from_csv.json")')
    print(f'  ключи в JSON: {list(people[0].keys())}')
    print(f'  строк в CSV: {len(csv_rows)}, объектов в JSON: {len(people)}')

    json_to_csv('data/samples/students.json', 'data/out/students_from_json.csv')
    print('\njson_to_csv("data/samples/students.json", "data/out/students_from_json.csv")')
    with open('data/out/students_from_json.csv', encoding='utf-8') as f:
        print(f.read().strip())

    print('\nПроверка ошибок:')
    bad_calls = [
        ('json_to_csv', 'data/samples/empty.json'),
        ('json_to_csv', 'data/samples/not_dicts.json'),
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
```

```bash
python src/lab05/json_csv.py
```

![Проверка модуля json_csv](../../images/lab05/img01.png)

*Рис. 1. Результат проверки функций `json_to_csv` и `csv_to_json`.*

## Задание B - CSV в XLSX `src/lab05/csv_xlsx.py`

### Функция `csv_to_xlsx`

Функция читает CSV через `csv.reader` и переносит все строки на лист `Sheet1` через `ws.append`. Первая строка - заголовок, она выделяется жирным шрифтом.

Ширина колонки считается по самому длинному значению в этой колонке, но не меньше 8 символов. К ширине добавляется 2 символа, чтобы текст не прилипал к границе ячейки.

```python
import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

MIN_WIDTH = 8


def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """Функция конвертирует CSV в XLSX

    Первая строка CSV - заголовок (выделяется жирным). Лист называется "Sheet1".
    Ширина каждой колонки подбирается по самому длинному значению, но не меньше 8 символов.

    Аргументы:
        csv_path: путь к входному CSV-файлу
        xlsx_path: путь к выходному XLSX-файлу

    Вывод:
        Ничего не возвращает, создаёт (или перезаписывает) XLSX-файл

    Ошибки:
        FileNotFoundError: если CSV-файла нет
        ValueError: неверный тип файла, пустой CSV, нет заголовка
            или строки разной длины
    """

    csv_file = Path(csv_path)
    xlsx_file = Path(xlsx_path)

    if csv_file.suffix.lower() != '.csv':
        raise ValueError(f'Неверный тип файла: {csv_file.name}, ожидается .csv')
    if xlsx_file.suffix.lower() != '.xlsx':
        raise ValueError(f'Неверный тип файла: {xlsx_file.name}, ожидается .xlsx')
    if not csv_file.is_file():
        raise FileNotFoundError(f'Файл не найден: {csv_file}')

    with open(csv_file, 'r', encoding='utf-8', newline='') as f:
        rows = list(csv.reader(f))

    if len(rows) == 0:
        raise ValueError('Пустой CSV')

    header = rows[0]
    if len(header) == 0 or '' in [name.strip() for name in header]:
        raise ValueError('В CSV нет заголовка или в нём есть пустая колонка')

    for i, row in enumerate(rows, start=1):
        if len(row) != len(header):
            raise ValueError(f'Неверная строка {i}: значений - {len(row)}, '
                             f'колонок в заголовке - {len(header)}')

    wb = Workbook()
    ws = wb.active
    ws.title = 'Sheet1'

    for row in rows:
        ws.append(row)

    for cell in ws[1]:
        cell.font = Font(bold=True)

    for col in range(len(header)):
        max_len = max(len(row[col]) for row in rows)
        width = max(max_len, MIN_WIDTH) + 2
        ws.column_dimensions[get_column_letter(col + 1)].width = width

    xlsx_file.parent.mkdir(parents=True, exist_ok=True)
    wb.save(xlsx_file)
```

Ошибки:

- файла нет - `FileNotFoundError`;
- неверное расширение входного или выходного файла - `ValueError`;
- пустой CSV или пустое название колонки в заголовке - `ValueError`;
- строки разной длины - `ValueError`.

### Проверка модуля

```python
if __name__ == '__main__':
    from openpyxl import load_workbook

    for src, dst in [('data/samples/people.csv', 'data/out/people.xlsx'),
                     ('data/samples/cities.csv', 'data/out/cities.xlsx')]:
        csv_to_xlsx(src, dst)
        ws = load_workbook(dst).active
        print(f'csv_to_xlsx("{src}", "{dst}")')
        print(f'  лист: {ws.title}, строк: {ws.max_row}, колонок: {ws.max_column}')
        widths = []
        for col in range(1, ws.max_column + 1):
            letter = get_column_letter(col)
            widths.append(f'{letter}={ws.column_dimensions[letter].width}')
        print(f'  ширина колонок: {", ".join(widths)}')

    print('\nПроверка ошибок:')
    for path in ['data/samples/empty.csv', 'data/samples/people.json',
                 'data/samples/bad_rows.csv', 'data/samples/nofile.csv']:
        try:
            csv_to_xlsx(path, 'data/out/bad.xlsx')
        except (ValueError, FileNotFoundError) as e:
            print(f'csv_to_xlsx("{path}", ...) -> {type(e).__name__}: {e}')
```

```bash
python src/lab05/csv_xlsx.py
```

![Проверка модуля csv_xlsx](../../images/lab05/img02.png)

*Рис. 2. Результат проверки функции `csv_to_xlsx`.*

## Сценарии демонстрации

### Сценарий 1. JSON в CSV

Входной файл `data/samples/people.json`:

```json
[
  {"name": "Анна", "age": 19, "city": "Москва", "email": "anna@mail.ru"},
  {"name": "Иван", "age": 20, "city": "Санкт-Петербург", "email": "ivan@yandex.ru"},
  {"name": "Мария", "age": 18, "city": "Казань", "email": "maria@gmail.com"},
  {"name": "Дмитрий", "age": 21, "city": "Новосибирск", "email": "dima@mail.ru"},
  {"name": "Елена", "age": 19, "city": "Екатеринбург", "email": "lena@yandex.ru"}
]
```

Результат `data/out/people_from_json.csv`:

```csv
name,age,city,email
Анна,19,Москва,anna@mail.ru
Иван,20,Санкт-Петербург,ivan@yandex.ru
Мария,18,Казань,maria@gmail.com
Дмитрий,21,Новосибирск,dima@mail.ru
Елена,19,Екатеринбург,lena@yandex.ru
```

Заголовок CSV совпадает с ключами объектов: `name,age,city,email`. В JSON 5 объектов, в CSV 5 строк с данными (без заголовка).

### Сценарий 2. JSON с разными полями

Собственный пример `data/samples/students.json`, где у объектов разный набор ключей:

```json
[
  {"name": "Олег", "group": "БИВТ-26-6", "score": 87},
  {"name": "Светлана", "group": "БИВТ-26-6"},
  {"name": "Павел", "score": 92, "phone": "+79001234567"}
]
```

Результат `data/out/students_from_json.csv`:

```csv
name,group,score,phone
Олег,БИВТ-26-6,87,
Светлана,БИВТ-26-6,,
Павел,,92,+79001234567
```

Колонки `name`, `group`, `score` взяты из первого объекта, колонка `phone` появилась только в третьем объекте и добавилась в конец. Отсутствующие значения заполнены пустой строкой.

### Сценарий 3. CSV в JSON

Входной файл `data/samples/people.csv`:

```csv
name,age,city,email
Анна,19,Москва,anna@mail.ru
Иван,20,Санкт-Петербург,ivan@yandex.ru
Мария,18,Казань,maria@gmail.com
Дмитрий,21,Новосибирск,dima@mail.ru
Елена,19,Екатеринбург,lena@yandex.ru
```

Результат `data/out/people_from_csv.json` (первые два объекта):

```json
[
  {
    "name": "Анна",
    "age": "19",
    "city": "Москва",
    "email": "anna@mail.ru"
  },
  {
    "name": "Иван",
    "age": "20",
    "city": "Санкт-Петербург",
    "email": "ivan@yandex.ru"
  },
  ...
]
```

Ключи в JSON совпадают с заголовком CSV, количество объектов (5) совпадает с количеством строк в CSV. Возраст записан строкой `"19"`, а не числом, так как значения из CSV сохраняются как строки.

### Сценарий 4. CSV в XLSX

```bash
python src/lab05/csv_xlsx.py
```

Из `data/samples/people.csv` получается `data/out/people.xlsx`, из `data/samples/cities.csv` - `data/out/cities.xlsx`. Файлы открываются в Excel, лист называется `Sheet1`, ширина колонок подобрана по длине текста.

![people.xlsx в Excel](../../images/lab05/img03.png)

*Рис. 3. Файл `data/out/people.xlsx`, открытый в Excel.*

![cities.xlsx в Excel](../../images/lab05/img04.png)

*Рис. 4. Файл `data/out/cities.xlsx`, открытый в Excel.*

### Файлы для проверки ошибок

| Файл | Что проверяет |
|---|---|
| `data/samples/empty.json` | пустой список `[]` |
| `data/samples/not_dicts.json` | в списке есть строка и число вместо словарей |
| `data/samples/empty.csv` | полностью пустой CSV |
| `data/samples/only_header.csv` | CSV только с заголовком |
| `data/samples/bad_rows.csv` | строка с меньшим количеством значений |