i = 0
total = 0
for i in range(1,101):
    if i % 3 == 0:
        continue
    else:
        total += i
print(f"1~100의 합계(3의 배수 제외) : {total}")