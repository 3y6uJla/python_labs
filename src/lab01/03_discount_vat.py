price = float(input('price: '))
discount = float(input('discount: '))
vat = float(input('vat: '))

base = price * (1 - discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount

print(f'{"База после скидки:":<20}{base:.2f} ₽')
print(f'{"НДС:":<20}{vat_amount:.2f} ₽')
print(f'{"Итого к оплате:":<20}{total:.2f} ₽')