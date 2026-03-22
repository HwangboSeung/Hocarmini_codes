def triple_number(number):
    return number * 3

def print_triple_number(number):
    print(triple_number(number))

def say_hello():
    print("Hello")

a = 2

b = triple_number(a)
c = triple_number(a)
d = triple_number(a) + triple_number(c)

print_triple_number(b)
say_hello()