CODE_S001 = "S001 Too long"

path = input()
with open(path, "r") as file:
    for index, line in enumerate(file.readlines(), start=1):
        if len(line.rstrip()) > 79:
            print(f"Line {index}: {CODE_S001}")
