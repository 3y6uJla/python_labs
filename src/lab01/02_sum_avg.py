# Задание 2

a,b = float(input('a: ').replace(',', '.')), float(input('b: ').replace(',', '.'))
sum = a+b
avg = sum/2
print(f'sum={sum:.2f}; avg={avg:.2f}')