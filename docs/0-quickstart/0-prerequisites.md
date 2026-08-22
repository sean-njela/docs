# Prerequisites

This project uses [`mise`](https://mise.jdx.dev/) for project tools and Python
environment management. The pinned tools are declared in `mise.toml` and
`mise.lock`.

## Required

- Git
- mise
- Python, uv, Task, and project tools installed through mise

Install Git and mise using your operating system's package manager or the
official installation instructions.

## Optional

Install Docker if you want to use the containerized MkDocs server or run the
GitHub workflows locally with `task test:ci`:

- [Docker installation guide](https://docs.docker.com/get-docker/)

## Clone and prepare the project

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
mise install
task setup
```

`task setup` runs `mise run setup`, which runs `uv sync` using the committed
`uv.lock`, and then installs the pre-commit hooks. `task test:ci` additionally
requires a running Docker daemon because it executes the event-driven GitHub
workflows through `act`.
