#Calculator

a = float(input("Введите а: "))
operation = input ("Введите операцию(+, -, *, /, **, sqrt): ")
b = float(input("Введите b: "))

if operation == "+":
    print(a + b)
elif operation == "-":
    print(a -b)
elif operation == "*":
    print(a * b)
elif operation == "/":
    print(a / b)
elif operation == "**":
    print(a ** b)
elif operation == "sqrt":
    print(a ** (1 / b))
else:
    print("ERROR")