# Main Taskfile Overview

This section describes the purpose and layout of the main `Taskfile.yml` used in this project. The Taskfile defines automation tasks to simplify development workflows and ensure consistency across environments.

## Purpose of This Taskfile

This Taskfile provides command-line shortcuts for tasks like:

- Project setup
- Development environment bootstrapping
- Application deployment
- Local documentation serving
- Cleanup and teardown

It abstracts repetitive shell commands into named tasks you can run with:

```bash
task <task-name>
```

## Core Sections

### 1. **Setup & Initialization**

Includes tasks for:

* Installing dependencies
* Setting up local development tools
* Generating keys or configs (if applicable)

### 2. **Development Workflow**

Common tasks for:

* Starting local services or dev containers
* Running dev servers
* Applying Kubernetes configs or local manifests
* Watching for file changes

### 3. **Documentation**

Tasks to serve the documentation locally through the Python environment or
Docker Compose. Project-specific documentation builds and publishing belong in
the project's own workflow tasks, not in this starter template.

### 4. **Quality & CI**

Run repository checks directly with `task check`, `uv run pytest -q`, and
`uv run mkdocs build --clean`. `task test:ci` runs the event-driven GitHub
workflows through `act` and requires the `act` CLI plus a running Docker
daemon. Local `act` execution covers the Ubuntu matrix leg; GitHub Actions
executes the complete Linux and macOS matrix.

### 5. **Deployment & Automation**

Tasks may automate:

* Building and pushing Docker images
* Running linters or formatters
* Applying infrastructure changes (e.g., with Terraform)

### 6. **Cleanup & Teardown**

Includes safe commands to:

* Tear down local clusters or containers
* Remove generated files or environments
* Reset state for fresh runs



## Typical Usage Flow

After configuring the project-specific extension points:

1. Install the versions declared in `mise.toml` and `mise.lock`:

   ```bash
   mise install
   ```

2. Sync Python dependencies and install repository hooks:

   ```bash
   task setup
   ```

3. Start development:

   ```bash
   task dev
   ```

4. Serve documentation:

   ```bash
   task docs
   ```

5. Clean up:

   ```bash
   task cleanup
   ```

## Notes

* To list all available tasks:

  ```bash
  task --list-all
  ```

* Variables and flags can be passed to tasks like so:

  ```bash
  task my-task <var>=<value>
  ```

* You can structure task dependencies using `deps:` and reuse shell logic cleanly across environments.

## Tips

| Key | Description |
|  |  |
| dotenv + env: | auto-load .env files and allow task-specific overrides. |
| vars: | static or dynamic variables (via shell) for templated substitution. |
| prompt: | even for setup or prod, ask user before proceeding. |
| preconditions: | enforce environment state before running. |
| deps: | define ordering (serial) via deps for safety and repeatability. |
| internal: | hide helper tasks from user listings. |
| platforms: | restrict tasks to specific OS/arch. |
| requires: | enforce required input variables. |
| status: | skip tasks if outputs already exist. |

## Related Docs

* [GitFlow Taskfile](./2-gitflow-taskfile.md)
* [Getting Started](../../0-quickstart/1-getting-started.md)
* [Architecture Overview](../../1-architecture/0-overview.md)

## Contact

For issues or suggestions related to automation and task structure, open an issue or contact the maintainer at [seannjela@outlook.com](mailto:seannjela@outlook.com).
