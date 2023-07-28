import ast
from pathlib import Path
import sys
import re

CODE_S001 = "S001 Too long"
CODE_S002 = "S002 Indentation is not a multiple of four"
CODE_S003 = "S003 Unnecessary semicolon after a statement (note that semicolons are acceptable in comments)"
CODE_S004 = "S004 Less than two spaces before inline comments"
CODE_S005 = "S005 TODO found (in comments only and case-insensitive)"
CODE_S006 = "S006 More than two blank lines preceding"
CODE_S007 = "S007 Too many spaces after construction_name (def or class)"
CODE_S008 = "S008 Class name should be written in CamelCase"
CODE_S009 = "S009 Function name should be written in snake_case"
CODE_S010 = "S010 Argument name arg_name should be written in snake_case"
CODE_S011 = "S011 Variable var_name should be written in snake_case"
CODE_S012 = "S012 The default argument value is mutable"


def get_sort_key(error):
    parts = error.split(": ")
    file_segment = parts[0]
    line_number = int(parts[1].split(" ")[1])
    return file_segment, line_number


class CodeAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.errors = []
        self.empty_lines = None
        self.line_num = None
        self.line = None
        with open(self.filename, "r") as file:
            self.ast = ast.parse(file.read())

    def run(self):
        for node in ast.walk(self.ast):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r"(_{0,2}[a-z_]+_{0,2})+", node.name):
                    self.errors.append(f"{self.filename}: Line {node.lineno}: {CODE_S009}")

                for arg in node.args.defaults:
                    if not isinstance(arg, ast.Constant):
                        self.errors.append(f"{self.filename}: Line {node.lineno}: {CODE_S012}")

                for arg in node.args.args:
                    if not re.match(r"([a-z_]+)+", arg.arg):
                        self.errors.append(f"{self.filename}: Line {arg.lineno}: {CODE_S010}")

            elif isinstance(node, ast.ClassDef):
                if not re.match(r"([A-Z][a-z()]+)+", node.name):
                    self.errors.append(f"{self.filename}: Line {node.lineno}: {CODE_S008}")

            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                if not re.match(r"([a-z_]+)+", node.id):
                    self.errors.append(f"{self.filename}: Line {node.lineno}: {CODE_S011}")

        with open(self.filename, "r") as file:
            self.empty_lines = 0
            for index, line in enumerate(file.readlines(), start=1):
                self.line_num = index
                self.line = line
                self.test_s001()
                self.test_s002()
                self.test_s003()
                self.test_s004()
                self.test_s005()
                self.test_s006()
                self.test_s007()

        for error in sorted(self.errors, key=get_sort_key):
            print(error)

    def test_s001(self):
        if len(self.line) > 79:
            self.errors.append(f"{self.filename}: Line {self.line_num}: {CODE_S001}")

    def test_s002(self):
        if len(self.line.strip()) == 0:
            return

        first_char = len(self.line) - len(self.line.lstrip())
        if first_char % 4 != 0:
            self.errors.append(f"{self.filename}: Line {self.line_num}: {CODE_S002}")

    def test_s003(self):
        statement = self.line.split('#')  # Divide statement and comment
        statement = statement[0].split("'")  # Divide for possible string
        statement = statement[-1].split('"')  # Divide for possible string
        if statement[-1].find(";") > 0:
            self.errors.append(f"{self.filename}: Line {self.line_num}: {CODE_S003}")

    def test_s004(self):
        if self.line.find("#") < 0 or self.line.startswith("#"):
            return

        statement = self.line.split('#')
        if len(statement[0]) - len(statement[0].rstrip()) < 2:
            self.errors.append(f"{self.filename}: Line {self.line_num}: {CODE_S004}")

    def test_s005(self):
        if self.line.find("#") < 0:
            return

        statement = self.line.split('#')
        if "todo" in statement[1].lower():
            self.errors.append(f"{self.filename}: Line {self.line_num}: {CODE_S005}")

    def test_s006(self):
        if len(self.line.strip()) == 0:
            self.empty_lines = self.empty_lines + 1
        elif len(self.line.strip()) > 0 and self.empty_lines > 2:
            self.empty_lines = 0
            self.errors.append(f"{self.filename}: Line {self.line_num}: {CODE_S006}")
        else:
            self.empty_lines = 0

    def test_s007(self):
        stripped = self.line.lstrip()
        if stripped.startswith("class") or stripped.startswith("def"):
            if re.match(r"(class|def)\s{2,}[A-Za-z()]+:", stripped):
                self.errors.append(f"{self.filename}: Line {self.line_num}: {CODE_S007}")


if __name__ == "__main__":
    args = sys.argv
    for path in args[1:]:
        if Path(path).is_file():
            code_analyzer_ast = CodeAnalyzer(path)
            code_analyzer_ast.run()
        else:
            for file in sorted([p for p in Path(path).iterdir()]):
                code_analyzer_ast = CodeAnalyzer(file)
                code_analyzer_ast.run()
