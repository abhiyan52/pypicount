import re
from .base_syntax import LanguageSyntax
from dataclasses import dataclass, asdict, field


@dataclass
class PythonLineVisitor:
    # Visitor class that tags a line and increments the count
    imports_count: int = field(init=False, default=0)
    print_statements: int = field(init=False, default=0)

    def visit(self, line):
        line = line.strip()
        if line.startswith("import"):
            self.imports_count += 1
        elif line.startswith("from"):
            self.imports_count += 1
        elif line.startswith("print("):
            self.print_statements += 1


class PythonSyntax(LanguageSyntax):

    def __init__(self, *args, **kwargs):
        super(PythonSyntax, self).__init__(*args, **kwargs)
        self.python_line_visitor = PythonLineVisitor()

    @classmethod
    def is_valid_extension(cls, extension):
        return extension == ".py"

    def is_blank(self, line):
        return not line.strip()

    def is_comment(self, line):
        return (
            line.strip().startswith('#')
            or re.match(r"(^(\"\"\").*(\"\"\")$)",  line.strip())
        )

    def is_code(self, line):
        is_code_line = not self.is_blank(line) and not self.is_comment(line)
        if is_code_line:
            self.python_line_visitor.visit(line)
        return is_code_line

    def is_multiline_comment(self, line):
        return (
            not self.is_comment(line)
            and (
                # Multiline comment start / end at beginning
                re.match(r"^(\"\"\")",  line)
                # Multiline comment end at the end of line
                or re.match(r".*(\"\"\")$", line)
            )
        )

    @property
    def extra(self):
        return asdict(self.python_line_visitor)
