list1 =[]
list2 = []
total =0
value =1
for i in range(0,4):
    for k in range(0,5):
        list1.append(total)
        total = value * 3
        value += 1
    list2.append(list1)

    list1=[]


print(list2)
