# Pypi Count

A lightweight, extensible module to count lines. Currently it supports python and java.

## Installation

Clone the repo to you local repo

```bash
git clone https://github.com/abhiyan52/pypicount.git

```

## Usage

```python
cd pypicount

# Install dependencies
pip install -r requirements.txt

# Run the module
python index.py <folderpath>

python index.py <filename>

```

## Contributing

Libraries used:

1. AsyncIO: Traversing the files and counting them concurrently for directories
2. PrettyTable: To print the output in tabular form


## Support for New Language

```python
# This is the base class for the parser
from syntax_parser.base_syntax import LanguageSyntax

# Override the methods 
class RustParser(LanguageSyntax):
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

```

## Screenshots

![alt text](https://github.com/abhiyan52/pypicount/blob/master/assets/file_test.png?raw=true)

![alt text](https://github.com/abhiyan52/pypicount/blob/master/assets/folder_read.png?raw=true)
