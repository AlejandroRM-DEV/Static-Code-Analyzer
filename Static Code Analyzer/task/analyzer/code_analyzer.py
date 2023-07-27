from pathlib import Path
import sys
import re


class CodeAnalyzer:
    CODE_S001 = "S001 Too long"
    CODE_S002 = "S002 Indentation is not a multiple of four"
    CODE_S003 = "S003 Unnecessary semicolon after a statement (note that semicolons are acceptable in comments)"
    CODE_S004 = "S004 Less than two spaces before inline comments"
    CODE_S005 = "S005 TODO found (in comments only and case-insensitive)"
    CODE_S006 = "S006 More than two blank lines preceding"
    CODE_S007 = "S007 Too many spaces after construction_name (def or class)"
    CODE_S008 = "S008 Class name should be written in CamelCase"
    CODE_S009 = "S009 Function name should be written in snake_case"

    def test_s001(self):
        if len(self.line) > 79:
            return f"{self.filename}: Line {self.line_num}: {self.CODE_S001}"
        else:
            return None

    def test_s002(self):
        if len(self.line.strip()) == 0:
            return None

        first_char = len(self.line) - len(self.line.lstrip())
        if first_char % 4 != 0:
            return f"{self.filename}: Line {self.line_num}: {self.CODE_S002}"
        else:
            return None

    def test_s003(self):
        statement = self.line.split('#')  # Divide statement and comment
        statement = statement[0].split("'")  # Divide for possible string
        statement = statement[-1].split('"')  # Divide for possible string
        if statement[-1].find(";") > 0:
            return f"{self.filename}: Line {self.line_num}: {self.CODE_S003}"
        else:
            return None

    def test_s004(self):
        if self.line.find("#") < 0 or self.line.startswith("#"):
            return None

        statement = self.line.split('#')
        if len(statement[0]) - len(statement[0].rstrip()) < 2:
            return f"{self.filename}: Line {self.line_num}: {self.CODE_S004}"
        else:
            return None

    def test_s005(self):
        if self.line.find("#") < 0:
            return None

        statement = self.line.split('#')
        if "todo" in statement[1].lower():
            return f"{self.filename}: Line {self.line_num}: {self.CODE_S005}"
        else:
            return None

    def test_s006(self):
        error = None
        if len(self.line.strip()) == 0:
            self.empty_lines = self.empty_lines + 1
        elif len(self.line.strip()) > 0 and self.empty_lines > 2:
            self.empty_lines = 0
            error = f"{self.filename}: Line {self.line_num}: {self.CODE_S006}"
        else:
            self.empty_lines = 0

        return error

    def test_s007(self):
        error = None
        stripped = self.line.lstrip()
        if stripped.startswith("class") or stripped.startswith("def"):
            if re.match(r"(class|def)\s{2,}[A-Za-z()]+:", stripped):
                error = f"{self.filename}: Line {self.line_num}: {self.CODE_S007}"

        return error

    def test_s008(self):
        error = None
        stripped = self.line.lstrip()
        if stripped.startswith("class"):
            if not re.match(r"class\s+([A-Z][a-z()]+)+:", stripped):
                error = f"{self.filename}: Line {self.line_num}: {self.CODE_S008}"

        return error

    def test_s009(self):
        error = None
        stripped = self.line.lstrip()
        if stripped.startswith("def"):
            if not re.match(r"def\s+(_{0,2}[a-z_]+_{0,2}[()]+)+:", stripped):
                error = f"{self.filename}: Line {self.line_num}: {self.CODE_S009}"

        return error

    def run(self):
        errors = []
        with open(self.filename, "r") as file:
            self.empty_lines = 0
            for index, line in enumerate(file.readlines(), start=1):
                self.line_num = index
                self.line = line
                errors.append(self.test_s001())
                errors.append(self.test_s002())
                errors.append(self.test_s003())
                errors.append(self.test_s004())
                errors.append(self.test_s005())
                errors.append(self.test_s006())
                errors.append(self.test_s007())
                errors.append(self.test_s008())
                errors.append(self.test_s009())

        for error in [error for error in errors if error is not None]:
            print(error)

    def __init__(self, filename):
        self.empty_lines = None
        self.line_num = None
        self.line = None
        self.filename = filename


if __name__ == "__main__":
    args = sys.argv
    for path in args[1:]:
        if Path(path).is_file():
            code_analyzer = CodeAnalyzer(path)
            code_analyzer.run()
        else:
            for file in sorted([p for p in Path(path).iterdir()]):
                code_analyzer = CodeAnalyzer(file)
                code_analyzer.run()
