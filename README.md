# Nassau Street Capital

An open source repository containing utility source code for quantitative finance and other software engineering builds for Nassau Street Capital, a student-run investment club at Princeton University.

## 📚 Table of Contents

- [🚀 Getting Started](#getting-started)
- [🤝 Contributing](#contributing)

## Getting started

To get started, you will need to create the nsc virtual environment.

1. Install Poetry (highly recommended)

```zsh
$ pip install poetry
```

2. Create the nsc virtual environment

```zsh
$ mkdir .venv
$ poetry config virtualenvs.in-project true
$ poetry shell
```

If **poetry** did not automatically activate the virtual environment for you, you can do so manually with

```zsh
$ source .venv/bin/activate
```

Note that will have to input the analogous command if you are not using the Unix terminal.

3. Install dependencies

```zsh
$ poetry install --no-root
```

**Alternative**: Non-poetry installation involves the following steps in the root directory:

```zsh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Without **poetry**, you are responsible for managing dependency versions.

## Contributing

If you're interested in contributing, please fork the repository and submit a pull request. For major changes, open an issue first.

## Developers (alphabetical by last name)

This repository is currently being maintained by

- Windsor Nguyen '25

## License

Nassau Street Capital is licensed under the terms of the [MIT License](LICENSE).
