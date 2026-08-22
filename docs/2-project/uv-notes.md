# uv Cheat Sheet

This project uses [`mise`](https://mise.jdx.dev/) to install and pin Python,
`uv`, and the other command-line tools declared in `mise.toml`. Keep
`mise.toml` and `mise.lock` as the source of truth instead of installing
project tools separately.

## Installation

From the repository root:

```bash
# Install the versions pinned in mise.toml and mise.lock
mise install

# Sync Python dependencies and install repository hooks
task setup

# Verify the managed tools
mise current
uv --version
```

Use the operating system package manager or the
[official Mise installation instructions](https://mise.jdx.dev/installing-mise.html)
to install Mise itself.

## Projects

```bash
# Create a new project in folder "myproj"
uv init myproj

# Create a new project in the current folder
uv init
```

## Dependencies

```bash
# Add a package
uv add requests

# Add a package with version
uv add django==4.2.7

# Add a development dependency
uv add --dev pytest

# Remove a package
uv remove requests
```

## Locking and Installing

```bash
# Install the pinned project tools and sync dependencies
mise install
task setup

# Sync after changing pyproject.toml
uv sync

# Update dependencies to the latest allowed versions
uv sync --upgrade

# Compile a requirements file from project metadata
uv pip compile pyproject.toml
```

`mise install` manages the project tool versions; `uv sync` manages the
Python environment and dependencies.

## Virtual Environments

The project virtual environment is created and maintained by `uv sync`,
which is run by `task setup`.

```bash
# Show the project environment path
uv venv --path

# Create a standalone environment for a separate project
uv venv --python 3.11
```


## Running Code

```bash
# Run Python inside environment
uv run python

# Run a script
uv run myscript.py

# Run a command with dependencies
uv run pytest
```

## Python Versions

The project's Python version is pinned in `mise.toml` and installed through
Mise:

```bash
# Show the versions managed by Mise
mise current
mise ls python

# Change the project pin, then install it
mise use python@3.14
mise install
```

Run `task setup` after changing the Python version so that `uv` recreates the
project environment with the selected interpreter.

## Inspecting

```bash
# Show dependency tree
uv tree

# Show project metadata
uv project show
```

## Building and Publishing

```bash
# Build source distribution and wheel
uv build

# Publish to PyPI (requires credentials)
uv publish
```

## Tools

Project-wide CLI tools belong in `mise.toml` so every contributor uses the
same versions:

```bash
# Install and list project-managed tools
mise install
mise ls

# Run a Python CLI declared in the project dependencies
uv run black --version

# Run a one-off Python CLI without installing it globally
uvx flake8 docs/
```

Use `uv tool run` or `uvx` for temporary Python tools; do not install a
project tool globally when it can be pinned in `mise.toml`.

## Useful Options

```bash
# Dry run, show what would happen
--dry-run

# Use lowest compatible versions
--resolution=lowest

# Target a different Python version when resolving
--python-version 3.10
```

Correct. The cheat sheet I gave did not include `uvx`. Here is the missing section.

## `uvx` Cheat Sheet

`uvx` is a shortcut to run any Python package or script **without pre-installing it**.
It automatically downloads the package into a temporary cache, runs it, and reuses cached copies on later runs.
It is like `npx` in Node.js.

## Syntax

```bash
uvx <package> [arguments...]
```

## Examples

```bash
# Run black without installing globally
uvx black myfile.py

# Run flake8
uvx flake8 src/

# Run httpie
uvx http --version

# Run Django admin script
uvx django-admin startproject mysite
```

## Pinning Versions

```bash
# Run a specific version of black
uvx black==23.9.1 --version
```

## With Python Scripts

```bash
# Run a Python script that is not installed
uvx -m http.server 8000
```

## Notes

* `uvx` installs packages into a cache under your user directory.
* First run is slower; later runs reuse the cache.
* If you need to clear the cache:

  ```bash
  uv cache clean
  ```

* Use `mise ls` to inspect project-managed tools.
* Use `uv tree` to inspect project dependencies.
* Use `uvx` or `uv tool run` for temporary Python tools that are not part of
  the project environment.

The project uses three distinct scopes:

| Scope | Command | What it manages | Source of truth |
| --- | --- | --- | --- |
| **Project tools** | `mise install`, `mise current` | Pinned Python and CLI tools | `mise.toml` + `mise.lock` |
| **Project dependencies** | `uv add`, `uv remove`, `uv sync` | Python packages | `pyproject.toml` + `uv.lock` |
| **Temporary Python tools** | `uvx` or `uv tool run` | One-off CLI packages | User cache |

Use `mise` for tools shared by the repository and `uv` for Python
dependencies and project commands.

With `uv`, you never edit `[tool.poetry.dependencies]` like in Poetry. You only use **standard PEP 621 fields** in `pyproject.toml`.

Two ways to add dependencies:

## 1. Let `uv` edit `pyproject.toml` for you

```bash
# Add a runtime dependency
uv add requests

# Add a dev dependency
uv add --dev pytest
```

This will:

* Update `pyproject.toml` under `[project]` or `[tool.uv]` (depending on context).
* Regenerate `uv.lock`.

## 2. Edit `pyproject.toml` manually

Minimal example with dependencies written by hand:

```toml
[project]
name = "myproj"
version = "0.1.0"
description = "Example project"
requires-python = ">=3.10"

dependencies = [
    "requests>=2.31",
    "flask>=2.3",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0",
]
```

Then run:

```bash
uv sync

# List installed packages (table)
uv pip list

# Freeze environment (pip-compatible format)
uv pip freeze
```

This will install what you declared and create/update `uv.lock`.

### Key difference from Poetry

* Poetry used `[tool.poetry.dependencies]` and `[tool.poetry.dev-dependencies]`.
* uv uses the **PEP 621 standard** `[project]` section for main dependencies.
* Dev dependencies live in `[tool.uv.dev-dependencies]`.
