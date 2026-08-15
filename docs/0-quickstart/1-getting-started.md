# Getting Started

## Prepare the environment

From the repository root:

```bash
mise install
task setup
```

`mise install` activates the versions pinned in `mise.toml` and `mise.lock`.
`task setup` runs `mise run setup` to synchronize the Python dependencies with
`uv`, then installs the pre-commit hooks.

## Run the project

Use the Taskfile for project workflows:

```bash
task --list-all
task setup
task status
task dev
```

Serve the documentation locally with one of these options:

```bash
# Local Python environment
task docs

# Containerized MkDocs server
task docs-docker
```

Run only one documentation server at a time. Open:

<http://127.0.0.1:8030/>

## Git Flow tasks

Git Flow automation is optional:

```bash
task -t Taskfile.gitflow.yml --list-all
task -t Taskfile.gitflow.yml <command>
```

## Cleanup

```bash
task cleanup-dev
task cleanup-all
```

See the [Tasks](../2-project/tasks/0-overview.md) section for the available
automation commands.


