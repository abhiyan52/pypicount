"""
    name: java_stntax.py
    author: abhiyanhaze
    description: File contains base abstract class Language Syntax to classify code syntax
"""


import re
from .base_syntax import LanguageSyntax


class JavaSyntax(LanguageSyntax):

    @classmethod
    def is_valid_extension(cls, extension):
        return extension == ".java"

    def is_blank(self, line):
        return not line.strip()

    def is_comment(self, line):
        return re.match(r"(\/\*.*\*\/)|(^\/\/)", line.strip())

    def is_code(self, line):
        return not self.is_blank(line) and not self.is_comment(line)

    def is_multiline_comment(self, line):
        return (
            not self.is_comment(line)
            and (
                re.match(r"^(\/\*).*",  line)
                or re.match(r".*\*\/$", line)
            )
        )
