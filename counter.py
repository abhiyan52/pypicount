"""
    author: abhiyanhaze
    description: Counter implementation logic are present in this file
"""

import os
from dataclasses import dataclass, field


@dataclass
class CounterResult:
    total_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    code_lines: int = 0
    extra: dict = field(init=True, default=dict)
    class_name: str = field(init=True, default=dict) # Identifying the language / file type

    def __add__(self, other):
        # Overriding add method to add multiple counts from files together
        for key, value in self.extra.items():
            if type(value) in (int, float,):
                self.extra[key] += other.extra[key]

        return CounterResult(
            total_lines=self.total_lines + other.total_lines,
            blank_lines=self.blank_lines + other.blank_lines,
            comment_lines=self.comment_lines + other.comment_lines,
            code_lines=self.code_lines + other.code_lines,
            class_name=self.class_name,
            extra=self.extra
        )


class LineCounter:

    def __init__(self, filepath, syntax):
        self.filepath = filepath
        self.syntax = syntax

    def count_lines(self):
        result = CounterResult(class_name=self.syntax.__class__.__name__)

        if not os.path.exists(self.filepath):
            return None

        with open(self.filepath, "r") as f:
            comment_context = False
            for line in f:
                result.total_lines += 1
                if self.syntax.is_blank(line):
                    result.blank_lines += 1
                elif comment_context:
                    result.comment_lines += 1
                    comment_context = not self.syntax.is_multiline_comment(
                        line
                    )
                    continue
                elif self.syntax.is_multiline_comment(line):
                    result.comment_lines += 1
                    comment_context = True
                elif self.syntax.is_comment(line):
                    result.comment_lines += 1
                elif self.syntax.is_code(line):
                    result.code_lines += 1
        result.extra = self.syntax.extra
        return result
