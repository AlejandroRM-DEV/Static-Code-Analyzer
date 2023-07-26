CODE_s001 = "S001 Too long"
CODE_s002 = "S002 Indentation is not a multiple of four"
CODE_s003 = "S003 Unnecessary semicolon after a statement (note that semicolons are acceptable in comments)"
CODE_s004 = "S004 Less than two spaces before inline comments"
CODE_s005 = "S005 TODO found (in comments only and case-insensitive)"
CODE_s006 = "S006 More than two blank lines preceding"


def test_s001(index, line):
    if len(line) > 79:
        return f"Line {index}: {CODE_s001}"
    else:
        return None


def test_s002(index, line):
    if len(line.strip()) == 0:
        return None

    first_char = len(line) - len(line.lstrip())
    if first_char % 4 != 0:
        return f"Line {index}: {CODE_s002}"
    else:
        return None


def test_s003(index, line):
    statement = line.split('#')  # Divide statement and comment
    statement = statement[0].split("'")  # Divide for possible string
    statement = statement[-1].split('"')  # Divide for possible string
    if statement[-1].find(";") > 0:
        return f"Line {index}: {CODE_s003}"
    else:
        return None


def test_s004(index, line):
    if line.find("#") < 0 or line.startswith("#"):
        return None

    statement = line.split('#')
    if len(statement[0]) - len(statement[0].rstrip()) < 2:
        return f"Line {index}: {CODE_s004}"
    else:
        return None


def test_s005(index, line):
    if line.find("#") < 0:
        return None

    statement = line.split('#')
    if "todo" in statement[1].lower():
        return f"Line {index}: {CODE_s005}"
    else:
        return None


if __name__ == "__main__":
    filename = input()
    with open(filename, "r") as file:
        empty_lines = 0
        errors = []
        for index, line in enumerate(file.readlines(), start=1):
            errors.append(test_s001(index, line))
            errors.append(test_s002(index, line))
            errors.append(test_s003(index, line))
            errors.append(test_s004(index, line))
            errors.append(test_s005(index, line))
            if len(line.strip()) == 0:
                empty_lines = empty_lines + 1
            elif len(line.strip()) > 0 and empty_lines > 2:
                errors.append(f"Line {index}: {CODE_s006}")
                empty_lines = 0
            else:
                empty_lines = 0

        errors = [error for error in errors if error is not None]
        for error in errors:
            print(error)
