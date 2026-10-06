def check_rectangular(mat: list[list[float | int]]) -> None:
    """Функция проверяет, что все строки матрицы одинаковой длины

    Ошибки:
        ValueError: если матрица "рваная"
    """

    for row in mat:
        if len(row) != len(mat[0]):
            raise ValueError('"Рваная" матрица')


def transpose(mat: list[list[float | int]]) -> list[list]:
    """Функция транспонирует матрицу

    Аргумент:
        Матрица - список списков чисел[цел./вещ.]

    Вывод:
        Транспонированная матрица (для пустой матрицы - [])

    Ошибки:
        ValueError: если матрица "рваная"
    """

    if not mat:
        return []
    check_rectangular(mat)
    res = []
    for j in range(len(mat[0])):
        col = []
        for i in range(len(mat)):
            col.append(mat[i][j])
        res.append(col)
    return res


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
    check_rectangular(mat)
    res = []
    for row in mat:
        total = 0
        for x in row:
            total += x
        res.append(total)
    return res


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
    check_rectangular(mat)
    res = []
    for j in range(len(mat[0])):
        total = 0
        for i in range(len(mat)):
            total += mat[i][j]
        res.append(total)
    return res


print('Примеры запуска:')
print(f'''
transpose

[[1, 2, 3]] -> {transpose([[1, 2, 3]])}
[[1], [2], [3]] -> {transpose([[1], [2], [3]])}
[[1, 2], [3, 4]] -> {transpose([[1, 2], [3, 4]])}
[] -> {transpose([])}
''')
## Запуск с ошибкой:
## print(f'[[1, 2], [3]] -> {transpose([[1, 2], [3]])}')

print(f'''
row_sums

[[1, 2, 3], [4, 5, 6]] -> {row_sums([[1, 2, 3], [4, 5, 6]])}
[[-1, 1], [10, -10]] -> {row_sums([[-1, 1], [10, -10]])}
[[0, 0], [0, 0]] -> {row_sums([[0, 0], [0, 0]])}
''')
## Запуск с ошибкой:
## print(f'[1, 2], [3]] -> {row_sums([[1, 2], [3]])}')
print(f'''
col_sums

[[1, 2, 3], [4, 5, 6]] -> {col_sums([[1, 2, 3], [4, 5, 6]])}
[[-1, 1], [10, -10]] -> {col_sums([[-1, 1], [10, -10]])}
[[0, 0], [0, 0]] -> {col_sums([[0, 0], [0, 0]])}
''')
## Запуск с ошибкой:
## print(f'[[1, 2], [3]] -> {col_sums([[1, 2], [3]])}')