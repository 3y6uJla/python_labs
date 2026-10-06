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
        raise ValueError('ФИ(О) должно состоять из 2-3 слов')
    if group == '':
        raise ValueError('Группа не может быть пустой')
    if gpa < 0 or gpa > 5:
        raise ValueError('GPA должен быть от 0.0 до 5.0')

    surname = parts[0].capitalize()
    initials = ''
    for name in parts[1:]:
        initials += name[0].upper() + '.'

    return f'{surname} {initials}, гр. {group}, GPA {gpa:.2f}'


print('Примеры запуска:')
print(f'''
format_record

("Иванов Иван Иванович", "BIVT-25", 4.6) -> {format_record(("Иванов Иван Иванович", "BIVT-25", 4.6))}
("Петров Пётр", "IKBO-12", 5.0) -> {format_record(("Петров Пётр", "IKBO-12", 5.0))}
("Петров Пётр Петрович", "IKBO-12", 5.0) -> {format_record(("Петров Пётр Петрович", "IKBO-12", 5.0))}
("  сидорова  анна   сергеевна ", "ABB-01", 3.999) -> {format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999))}
''')
# Примеры, которые выводят ошибку ValueError:
# print(f'("", "ABB-01", 4.0) -> {format_record(("", "ABB-01", 4.0))}')
# print(f'("Иванов Иван", "", 4.0) -> {format_record(("Иванов Иван", "", 4.0))}')
# print(f'("Иванов Иван", "ABB-01", 5.1) -> {format_record(("Иванов Иван", "ABB-01", 5.1))}')
# Пример, который выводит ошибку TypeError:
# print(f'("Иванов Иван", "ABB-01", "5") -> {format_record(("Иванов Иван", "ABB-01", "5"))}')