#(VALORE - MIN) / (MAX - MIN) * 100

list_n = [0,1,2,3,4,5,6,7,8,9,10]

value_min = min(list_n)
print(value_min)

value_max = max(list_n)
print(value_max)

print('-------------')
new_list = []

for value in list_n:
    new_min = value - value_min
    max_min = value_max - value_min
    result = (new_min / max_min) *100
    print(result)
    new_list.append(result)

print(list_n)
print(new_list)
