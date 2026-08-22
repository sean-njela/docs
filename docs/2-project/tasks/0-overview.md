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
```

For detailed details about taskfile use:

* [Main Taskfile](./1-main-taskfile.md)
* [GitFlow Taskfile](./2-gitflow-taskfile.md)


## Contact

Questions or issues with GitFlow setup? Reach out via [GitHub Issues](https://github.com/your-username/your-repo/issues) or email at [your.email@example.com](mailto:your.email@example.com).
