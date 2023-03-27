from syntax_parser.java_syntax import JavaSyntax
from syntax_parser.python_syntax import PythonSyntax


class LanguageSyntaxRegistry:
    _registry = {}
    _initialized = False

    @classmethod
    def register(cls, syntax_class):
        cls._registry[syntax_class.__name__] = syntax_class

    @classmethod
    def get_syntax(cls, extension):
        for class_name, klass in cls._registry.items():
            syantax_handler = klass.is_valid_extension(extension)
            if syantax_handler:
                return klass
        return None

    @classmethod
    def initialize(cls, load_default=False):
        cls._initialized = True
        if load_default:
            cls.register(PythonSyntax)
            cls.register(JavaSyntax)
