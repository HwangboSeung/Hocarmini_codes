number_list = [3, 5, 6, -8, 156]
number = number_list[4]
print(number)

number_list[4] = 3
number_list.append(34)
#print(number_list)

new_list = []

for number in number_list:
    #print(number)
    new_list.append(number)

print(new_list)