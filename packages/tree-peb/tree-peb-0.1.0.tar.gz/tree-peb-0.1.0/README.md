# Directory Tree

List contents of directories in tree-like format.

## Installation

## Example

```text
$ python .\tree.py
.\
|
├── tree\
│   ├── __init__.py
│   ├── cli.py
│   └── tree_util.py
│
├── LICENSE
├── README.md
└── tree.py
```

## CLI Options

```text
usage: tree [-h] [-v] [-d] [-o OUTPUT_FILE] [ROOT_DIR]

positional arguments:
  ROOT_DIR              Generate a full directory tree from the given ROOT_DIR

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d, --dir-only        Generate a directory-only tree
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Store the tree output in a file
```
