import re

# your code here
name = input()

if re.match(r"^[B-N][AEIOUaeiou]", name):
    print("Suitable!")
