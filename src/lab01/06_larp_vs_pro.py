N = int(input(f'Введите кол-во перваков: '))
crowd = []

for _ in range(N):        
    surname, name, age, larp_or_pro = input().split()        
    crowd.append({
    "surname": surname,
    "name": name,
    "age": int(age),
    "larp_or_pro": larp_or_pro.lower()=='true'
    })

result = sum(student["larp_or_pro"] == 1 for student in crowd)

print(result, N-result)

