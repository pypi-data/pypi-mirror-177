# Pylint Per File Ignores!

This pylint plugin will enable per-file-ignores in your project!

## Install

```
# w/ poetry
poetry add --dev pylint-per-file-ignores

# w/ pip
pip install pylint-per-file-ignores
```

## Add to Pylint Settings

Edit your `pyproject.toml`:

```
[tool.pylint.MASTER]
load-plugins=[
    "pylint-per-file-ignores",
    ...
]
```


## Usage

Add a section to your `pyproject.toml` with the patterns and codes you would like to ignore.

```
[tool.pylint-per-file-ignores]
"/folder_1/"="missing-function-docstring,W0621,W0240,C0115"
"file.py"="C0116,E0001"
```