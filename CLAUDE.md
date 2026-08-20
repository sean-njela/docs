# Repository Guidelines

This repository is the evolving starting point for open-source projects. It provides a reusable documentation, tooling, and automation foundation that can be adapted as each new project is created; it is intentionally not a finished product.

Authored Markdown under `docs/` is rendered as a Material for MkDocs site. The repository also contains Taskfile automation, Git Flow helpers, environment lockfiles, and optional Docker support.

There is currently no application source tree (`src/`, `app/`, or `lib/`), JavaScript/TypeScript package, installable Python package, or implemented service runtime. `README.md` and parts of the documentation retain generic template text and placeholder URLs; treat them as starting-point material and update them as the repository evolves.

## Architecture & Data Flow

The implemented architecture is a documentation toolchain:

1. `mise install` provisions the pinned CLI tools from `mise.toml`/`mise.lock`.
2. `task setup` runs `mise run setup` (`uv sync`) and installs pre-commit hooks.
3. `uv` manages the non-package Python environment described by `pyproject.toml`/`uv.lock`.
4. `mkdocs.yml` reads Markdown from `docs/`, applies the Material theme and configured extensions/plugins, and serves the site locally or writes generated output under `site/`.
5. `task docs-docker` provides the alternative Docker Compose path (host `8030` to container `8000`). Versioned publishing is wired into optional Git Flow tasks through `mike`.

`docs/1-architecture/0-overview.md` contains hypothetical Terraform/Argo CD/image-updater/Slack examples. Treat those as documentation placeholders, not as implemented components or data flow.

## Key Directories

- `docs/` — authored Markdown, organized by numeric prefixes such as `0-quickstart/`, `1-architecture/`, `2-project/`, `3-troubleshooting/`, and `4-about/`.
- `site/` — generated MkDocs output; ignored by Git and normally should not be edited by hand.
- `assets/` — media and generated/compressed demo assets.
- `.github/workflows/` — currently only the manual Git Flow branch-protection workflow.
- `branch-rules/` — checked-in GitHub branch ruleset JSON examples.
- Root configuration — `mkdocs.yml`, `Taskfile.yml`, `Taskfile.gitflow.yml`, `mise.toml`, `pyproject.toml`, and lockfiles.

There are no standalone `scripts/` or repository-owned test directories.

## Development Commands

Run commands from the repository root:

```bash
mise install                 # install pinned tools
task setup                   # sync uv environment and install hooks
task --list-all              # list available Task tasks
task docs                   # serve MkDocs at http://127.0.0.1:8030
task docs-docker            # serve docs through Docker Compose
task cleanup-dev            # stop the docs container
task precommit              # run configured hooks, when configuration exists
```

`task docs` and `task docs-docker` are alternative servers—run only one at a time. `task versions` lists `mike` versions. Media tasks accept variables, for example `task compress video=path/to/input.mp4`.

`dev`, `prod`, `status`, and `cleanup-prod` are currently described in `Taskfile.yml` but have no commands. Do not assume they provision or deploy anything. `Taskfile.gitflow.yml` contains branch, commit, push, release, hotfix, and `gh-pages` operations; these mutate local and remote Git state and require explicit intent before use.

## Code Conventions & Common Patterns

- Keep documentation navigation and directory ordering aligned with the numeric prefixes in `docs/` and the `nav` section of `mkdocs.yml`.
- Use Markdown headings, fenced code blocks, and paths/commands that match the actual repository. Update `mkdocs.yml` when adding a page that should be published.
- Task names are lowercase and hyphenated (`cleanup-dev`, `docs-docker`); Task variables are uppercase (`PROJECT_NAME`, `MKDOCS_PORT`).
- `Taskfile.yml` automatically loads `.env` and `.env.local`; both are ignored by Git. Do not commit secrets or machine-specific values.
- Python is used for MkDocs tooling only. There are no application async, state-management, dependency-injection, or service error-handling patterns to imitate.
- Prefer the pinned local tools and existing Task/mise workflows over ad-hoc global installations.
- Be careful with generic or aspirational documentation: some task pages describe examples that are not implemented, and `mkdocs.yml` references `docs/includes/mkdocs.md`, which may be absent.

## Important Files

- `mkdocs.yml` — site metadata, Material theme, plugins/extensions, Markdown navigation, Mermaid support, and version selector.
- `Taskfile.yml` — primary setup, docs-serving, Docker, cleanup, pre-commit, and asset tasks.
- `Taskfile.gitflow.yml` — optional stateful Git Flow and documentation release automation.
- `mise.toml` / `mise.lock` — pinned tool versions and the `setup` task.
- `pyproject.toml` / `uv.lock` — Python requirement, MkDocs dependencies, and locked environment.
- `docker-compose.mkdocs.yml` / `Dockerfile` — containerized docs server.
- `docs/0-quickstart/` — setup and local workflow instructions.
- `.github/workflows/gitflow-protect.yaml` — manual GitHub ruleset API automation; it is not a test or build pipeline.

## Runtime/Tooling Preferences

Use mise as the source of truth for tool versions: Python `3.14.7`, uv `0.12.4`, Task `3.52.0`, git-flow-next `2.0.0`, ffmpeg `9.0.1`, pre-commit `4.6.2`, and act `0.2.89`. The project declares Python `>=3.12` and uses uv with `package = false`; it is not an installable Python application.

Use `uv run ...` for Python/MkDocs commands after `task setup`. Docker is optional and is only needed for the containerized docs workflow. `Dockerfile` uses an unpinned `mkdocs-material:latest` base image, so prefer the mise/uv local workflow when reproducibility matters.

## Testing & QA

No repository-owned `tests/` or `test/` suite, fixtures, coverage configuration, or test/lint CI jobs currently exists. `pytest` and `black` are declared as development dependencies in `pyproject.toml`, but there is no pytest configuration or coverage threshold. If tests are added, keep them in a repository-owned test directory and run them through the uv environment (for example, `uv run pytest`).

`task precommit` invokes `pre-commit run --all-files` using the shared `.pre-commit-config.yaml`. The hooks validate JSON, TOML, and YAML (excluding `mkdocs.yml`, which uses a deliberate Python YAML tag), reject merge conflicts, oversized additions, private keys, and case collisions. The sole GitHub workflow is manually dispatched branch-protection API automation and does not validate documentation, tests, formatting, or builds.

For documentation changes, the practical smoke check is to run `task docs`, open the local site at port `8030`, and inspect the changed navigation/page. Avoid `repomix`'s `--no-security-check` mode for sensitive material and do not run Git Flow commit/push/release operations unless explicitly requested.
