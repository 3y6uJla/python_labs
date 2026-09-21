N = int(input(f'in_1: '))
crowd = []

for i in range(N):        
    surname, name, age, larp_or_pro = input(f'in_{i+2}: ').split()        
    crowd.append({
    "surname": surname,
    "name": name,
    "age": int(age),
    "larp_or_pro": larp_or_pro.lower()=='true'
    })

result = sum(student["larp_or_pro"] == 1 for student in crowd)

print(f'out: {result} {N-result}')