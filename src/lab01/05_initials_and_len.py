# Задание 5

fio = input('ФИО: ').split()
print(f'Инициалы: {fio[0][0]}{fio[1][0]}{fio[2][0]}.')

fio = ' '.join(fio)
print(len(fio))