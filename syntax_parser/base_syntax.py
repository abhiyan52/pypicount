"""
    name: base_syantax.py
    author: abhiyanhaze
    description: File contains base abstract class Language Syntax to classify code syntax
"""

from abc import ABC, abstractmethod


class LanguageSyntax(ABC):
    # Abstract class for implementing language syntax

    @classmethod
    def is_valid_extension(cls, filename):
        raise NotImplementedError(
            "The member must implement is_valid_extension class method"
        )

    @abstractmethod
    def is_blank(self, line):
        pass

    @abstractmethod
    def is_comment(self, line):
        pass

    @abstractmethod
    def is_code(self, line):
        pass

    @abstractmethod
    def is_multiline_comment(self, line):
        pass

    @property
    def extra(self):
        return {}
