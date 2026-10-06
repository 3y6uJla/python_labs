# Лабораторная работа №2

## Задание A. arrays.py

### min_max

```python
def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """Функция возвращает минимум и максимум списка

    Аргумент:
        Список чисел[цел./вещ.]

    Вывод:
        Кортеж(мин. списка, макс. списка)

    Ошибки:
        ValueError: если список пуст
    """

    if len(nums) == 0:
        raise ValueError('Список пуст')

    lo = nums[0]
    hi = nums[0]
    for x in nums:
        if x < lo:
            lo = x
        if x > hi:
            hi = x
    return lo, hi
```

```
[3, -1, 5, 5, 0] -> (-1, 5)
[42] -> (42, 42)
[-5, -2, -9] -> (-9, -2)
[1.5, 2, 2.0, -3.1] -> (-3.1, 2)
```

Примеры с ошибками:

```
[] -> ValueError: Список пуст
```

### unique_sorted

```python
def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """Функция возвращает отсортированный список уникальных значений

    Аргумент:
        Список чисел[цел./вещ.]

    Вывод:
        Список[уникальные значения по возрастанию]
    """

    res = list(set(nums))

    for i in range(len(res)):
        for j in range(len(res) - 1 - i):
            if res[j] > res[j + 1]:
                res[j], res[j + 1] = res[j + 1], res[j]
    return res
```

```
[3, 1, 2, 1, 3] -> [1, 2, 3]
[] -> []
[-1, -1, 0, 2, 2] -> [-1, 0, 2]
[1.0, 1, 2.5, 2.5, 0] -> [0, 1.0, 2.5]
```

### flatten

```python
def flatten(mat: list[list | tuple]) -> list:
    """Функция "расплющивает" матрицу в вектор

    Аргумент:
        Список списков/кортежей

    Вывод:
        Вектор из элементов списков списка

    Ошибки:
        TypeError: если строка матрицы - не список/кортеж
    """

    res = []
    for row in mat:
        if not isinstance(row, (list, tuple)):
            raise TypeError('Строка не строка строк матрицы')
        res.extend(row)
    return res
```

```
[[1, 2], [3, 4]] -> [1, 2, 3, 4]
[[1, 2], (3, 4, 5)] -> [1, 2, 3, 4, 5]
[[1], [], [2, 3]] -> [1, 2, 3]
```

Примеры с ошибками:

```
[[1, 2], "ab"] -> TypeError: Строка не строка строк матрицы
```

## Задание B. matrix.py

### _check_rectangular

```python
def _check_rectangular(mat: list[list[float | int]]) -> None:
    """Проверяет, что все строки матрицы одинаковой длины

    Ошибки:
        ValueError: если матрица "рваная"
    """

    for row in mat:
        if len(row) != len(mat[0]):
            raise ValueError('"Рваная" матрица')
```

### transpose

```python
def transpose(mat: list[list[float | int]]) -> list[list]:
    """Функция транспонирует матрицу (строки становятся столбцами)

    Аргумент:
        Матрица - список списков чисел[цел./вещ.]

    Вывод:
        Транспонированная матрица (для пустой матрицы - [])

    Ошибки:
        ValueError: если матрица "рваная"
    """

    if not mat:
        return []
    _check_rectangular(mat)
    res = []
    for j in range(len(mat[0])):
        col = []
        for i in range(len(mat)):
            col.append(mat[i][j])
        res.append(col)
    return res
```

```
[[1, 2, 3]] -> [[1], [2], [3]]
[[1], [2], [3]] -> [[1, 2, 3]]
[[1, 2], [3, 4]] -> [[1, 3], [2, 4]]
[] -> []
```

Примеры с ошибками:

```
[[1, 2], [3]] -> ValueError: "Рваная" матрица
```

### row_sums

```python
def row_sums(mat: list[list[float | int]]) -> list[float]:
    """Функция считает сумму по каждой строке матрицы

    Аргумент:
        Матрица - список списков чисел[цел./вещ.]

    Вывод:
        Список сумм строк

    Ошибки:
        ValueError: если матрица пустая или "рваная"
    """

    if not mat:
        raise ValueError('Пустая матрица')
    _check_rectangular(mat)
    res = []
    for row in mat:
        total = 0
        for x in row:
            total += x
        res.append(total)
    return res
```

```
[[1, 2, 3], [4, 5, 6]] -> [6, 15]
[[-1, 1], [10, -10]] -> [0, 0]
[[0, 0], [0, 0]] -> [0, 0]
```

Примеры с ошибками:

```
[[1, 2], [3]] -> ValueError: "Рваная" матрица
[] -> ValueError: Пустая матрица
```

### col_sums

```python
def col_sums(mat: list[list[float | int]]) -> list[float]:
    """Функция считает сумму по каждому столбцу матрицы

    Аргумент:
        Матрица - список списков чисел[цел./вещ.]

    Вывод:
        Список сумм столбцов

    Ошибки:
        ValueError: если матрица пустая или "рваная"
    """

    if not mat:
        raise ValueError('Пустая матрица')
    _check_rectangular(mat)
    res = []
    for j in range(len(mat[0])):
        total = 0
        for i in range(len(mat)):
            total += mat[i][j]
        res.append(total)
    return res
```

```
[[1, 2, 3], [4, 5, 6]] -> [5, 7, 9]
[[-1, 1], [10, -10]] -> [9, -9]
[[0, 0], [0, 0]] -> [0, 0]
```

Примеры с ошибками:

```
[[1, 2], [3]] -> ValueError: "Рваная" матрица
[] -> ValueError: Пустая матрица
```

## Задание C. tuples.py

### format_record

```python
def format_record(rec: tuple[str, str, float]) -> str:
    """Функция форматирует запись студента в строку

    Аргумент:
        Кортеж(ФИО, группа, GPA)

    Вывод:
        Строка вида "Фамилия И.О., гр. ГРУППА, GPA 0.00"

    Ошибки:
        TypeError: если ФИО/группа - не строки или GPA - не число
        ValueError: если в кортеже не 3 элемента, ФИО не из 2-3 слов,
                    группа пустая или GPA вне диапазона 0.0..5.0
    """

    if len(rec) != 3:
        raise ValueError('В кортеже должно быть 3 элемента')
    fio, group, gpa = rec

    if not isinstance(fio, str) or not isinstance(group, str):
        raise TypeError('ФИО и группа должны быть строками')
    if not isinstance(gpa, (int, float)):
        raise TypeError('GPA должен быть числом')

    parts = fio.split()
    group = group.strip()

    if len(parts) < 2 or len(parts) > 3:
        raise ValueError('ФИО должно состоять из 2 или 3 слов')
    if group == '':
        raise ValueError('Группа не может быть пустой')
    if gpa < 0 or gpa > 5:
        raise ValueError('GPA должен быть от 0.0 до 5.0')

    surname = parts[0].capitalize()
    initials = ''
    for name in parts[1:]:
        initials += name[0].upper() + '.'

    return f'{surname} {initials}, гр. {group}, GPA {gpa:.2f}'
```

```
("Иванов Иван Иванович", "BIVT-25", 4.6) -> Иванов И.И., гр. BIVT-25, GPA 4.60
("Петров Пётр", "IKBO-12", 5.0) -> Петров П., гр. IKBO-12, GPA 5.00
("Петров Пётр Петрович", "IKBO-12", 5.0) -> Петров П.П., гр. IKBO-12, GPA 5.00
("  сидорова  анна   сергеевна ", "ABB-01", 3.999) -> Сидорова А.С., гр. ABB-01, GPA 4.00
```

Примеры с ошибками:

```
("", "ABB-01", 4.0) -> ValueError: ФИО должно состоять из 2 или 3 слов
("Иванов Иван", "", 4.0) -> ValueError: Группа не может быть пустой
("Иванов Иван", "ABB-01", 5.1) -> ValueError: GPA должен быть от 0.0 до 5.0
("Иванов Иван", "ABB-01", "5") -> TypeError: GPA должен быть числом
```