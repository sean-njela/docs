# Overview

This Taskfile defines automation tasks to simplify development workflows and
ensure consistency across environments. Project tools are installed and
pinned by Mise; Task provides the project commands that run after setup.

From the repository root, prepare the environment with:

```bash
mise install
task setup
```

It abstracts repetitive shell commands into named tasks you can run with:

```bash
task <task-name> # runs a task
```

You can list all available tasks with:

```bash
task --list-all

## CI and regression checks

Run the lightweight local checks with:

```bash
task check
uv run pytest -q
uv run mkdocs build --clean
```

Run the event-driven GitHub workflows locally with:

```bash
task test:ci
```

This task requires both the `act` CLI and a running Docker daemon. It runs the
Ubuntu matrix leg for `push` and `pull_request`; GitHub Actions runs the
complete Linux and macOS matrix. The manual branch-protection workflow is not
executed locally because it changes GitHub rulesets.
```

For detailed details about taskfile use:

* [Main Taskfile](./1-main-taskfile.md)
* [GitFlow Taskfile](./2-gitflow-taskfile.md)


## Contact

Questions or issues with GitFlow setup? Reach out via [GitHub Issues](https://github.com/your-username/your-repo/issues) or email at [your.email@example.com](mailto:your.email@example.com).
