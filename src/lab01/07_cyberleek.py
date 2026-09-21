string = input(f'in: ')
result = ''

for i in range(len(string)):
    if string[i].lower()!=string[i]:
        first_index = i
        break

for i in range(len(string)):
    if string[i].isdigit():
        step = abs(first_index-(i+1))
        break

for i in range(first_index,len(string),step):
    result += string[i]

print(f'out: {result}')