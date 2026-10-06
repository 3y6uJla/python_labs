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


print('Примеры запуска:')
print(f'''
min_max

[3, -1, 5, 5, 0] -> {min_max([3, -1, 5, 5, 0])}
[42] -> {min_max([42])}
[-5, -2, -9] -> {min_max([-5, -2, -9])}
[1.5, 2, 2.0, -3.1] -> {min_max([1.5, 2, 2.0, -3.1])}
''')
# Пример, который выводит ошибку ValueError:
# print(f'[] -> {min_max([])}')

print(f'''
unique_sorted

[3, 1, 2, 1, 3] -> {unique_sorted([3, 1, 2, 1, 3])}
[] -> {unique_sorted([])}
[-1, -1, 0, 2, 2] -> {unique_sorted([-1, -1, 0, 2, 2])}
[1.0, 1, 2.5, 2.5, 0] -> {unique_sorted([1.0, 1, 2.5, 2.5, 0])}
''')

print(f'''
flatten

[[1, 2], [3, 4]] -> {flatten([[1, 2], [3, 4]])}
[[1, 2], (3, 4, 5)] -> {flatten([[1, 2], (3, 4, 5)])}
[[1], [], [2, 3]] -> {flatten([[1], [], [2, 3]])}
''')
# Пример, который выводит ошибку TypeError:
# print(f'[[1, 2], "ab"] -> {flatten([[1, 2], "ab"])}')