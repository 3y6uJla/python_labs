import re

WORD_RE = re.compile(r'\w+(?:-\w+)*')


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    """Функция нормализует строку

    Аргументы:
        text: исходная строка
        casefold: True - привести к casefold, False - к lower
        yo2e: True - заменить все ё/Ё на е/Е

    Вывод:
        Нормализованная строка: пробелы, табуляции и переносы строк схлопнуты в один пробел, края обрезаны

    Ошибки:
        TypeError: если text не строка
    """

    if not isinstance(text, str):
        raise TypeError('text должен быть строкой')

    text = text.casefold() if casefold else text.lower()

    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')

    return ' '.join(text.split())


def tokenize(text: str) -> list[str]:
    """Функция разбивает текст на слова

    Слово - последовательность символов \\w (буквы/цифры/подчёркивание), внутри слова допускается дефис (например, "по-настоящему"). Числа считаются словами, эмодзи и знаки препинания - разделители.

    Аргумент:
        text: строка (предполагается, что уже нормализована)

    Вывод:
        Список слов в порядке появления в тексте

    Ошибки:
        TypeError: если text не строка
    """

    if not isinstance(text, str):
        raise TypeError('text должен быть строкой')

    return WORD_RE.findall(text)


def count_freq(tokens: list[str]) -> dict[str, int]:
    """Функция считает частоты слов

    Аргумент:
        tokens: список токенов

    Вывод:
        Словарь слово -> количество вхождений
    """

    freq: dict[str, int] = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Функция возвращает топ-N слов по частоте

    Аргументы:
        freq: словарь слово -> частота
        n: сколько слов вернуть (по умолчанию 5)

    Вывод:
        Список пар (слово, частота), отсортированный по убыванию частоты,
        при равенстве частот - по алфавиту слова

    Ошибки:
        ValueError: если n отрицательное
    """

    if n < 0:
        raise ValueError('n не может быть отрицательным')

    items = sorted(freq.items(), key=lambda pair: (-pair[1], pair[0]))
    return items[:n]


def check(call: str, got: object, expected: object) -> None:
    """Функция выводит результат вызова и проверяет его через assert

    Аргументы:
        call: текст вызова для вывода
        got: полученный результат
        expected: ожидаемый результат
    """

    print(f'{call} -> {got!r}')
    assert got == expected, f'ожидалось {expected!r}'


if __name__ == '__main__':
    print('normalize:')
    check('normalize("ПрИвЕт\\nМИр\\t")', normalize("ПрИвЕт\nМИр\t"), "привет мир")
    check('normalize("ёжик, Ёлка")', normalize("ёжик, Ёлка"), "ежик, елка")
    check('normalize("Hello\\r\\nWorld")', normalize("Hello\r\nWorld"), "hello world")
    check('normalize("  двойные   пробелы  ")',
          normalize("  двойные   пробелы  "), "двойные пробелы")

    print('\ntokenize:')
    check('tokenize("привет мир")', tokenize("привет мир"), ["привет", "мир"])
    check('tokenize("hello,world!!!")', tokenize("hello,world!!!"), ["hello", "world"])
    check('tokenize("по-настоящему круто")',
          tokenize("по-настоящему круто"), ["по-настоящему", "круто"])
    check('tokenize("2025 год")', tokenize("2025 год"), ["2025", "год"])
    check('tokenize("emoji 😀 не слово")',
          tokenize("emoji 😀 не слово"), ["emoji", "не", "слово"])

    print('\ncount_freq + top_n:')
    tokens = ["a", "b", "a", "c", "b", "a"]
    freq = count_freq(tokens)
    check(f'count_freq({tokens})', freq, {"a": 3, "b": 2, "c": 1})
    check('top_n(freq, 2)', top_n(freq, 2), [("a", 3), ("b", 2)])

    tokens2 = ["bb", "aa", "bb", "aa", "cc"]
    freq2 = count_freq(tokens2)
    check(f'count_freq({tokens2})', freq2, {"aa": 2, "bb": 2, "cc": 1})
    check('top_n(freq2, 2)', top_n(freq2, 2), [("aa", 2), ("bb", 2)])

    print('\nВсе тесты пройдены')