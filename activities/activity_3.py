def get_max_value_from_number_list(number_list):
    max_value = 0
    for number in number_list:
        if number > max_value:
            max_value = number
    return max_value

number_list = [3, 5, 78, -7, 45]
max_value = get_max_value_from_number_list(number_list)
        
print("Max value is " + str(max_value))