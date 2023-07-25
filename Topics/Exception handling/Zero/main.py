n = int(input())
denominator = int(input())
try:
    result = n // denominator
except ZeroDivisionError:
    print("Division by zero is not supported")
else:
    print(result)

