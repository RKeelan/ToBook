# ToBook

[![PyPI](https://img.shields.io/pypi/v/ToBook.svg)](https://pypi.org/project/ToBook/)
[![Changelog](https://img.shields.io/github/v/release/RKeelan/ToBook?include_prereleases&label=changelog)](https://github.com/RKeelan/ToBook/releases)
[![Tests](https://github.com/RKeelan/ToBook/actions/workflows/test.yml/badge.svg)](https://github.com/RKeelan/ToBook/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/RKeelan/ToBook/blob/master/LICENSE)

Convert various kinds of document into an ebook

## Installation

Install this tool using `pip`:
```bash
pip install ToBook
```
## Usage

For help, run:
```bash
ToBook --help
```
You can also use:
```bash
python -m ToBook --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd ToBook
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
