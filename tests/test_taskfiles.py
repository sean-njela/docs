from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TASK = shutil.which("task")


@pytest.fixture
def task_command() -> str:
    if TASK is None:
        pytest.fail("Task CLI is required to test the Taskfiles")
    return TASK


def run_task(
    task_command: str,
    *args: str,
    cwd: Path,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    process_env = os.environ.copy()
    if env:
        process_env.update(env)
    return subprocess.run(
        [task_command, "--dir", str(cwd), *args],
        cwd=cwd,
        env=process_env,
        capture_output=True,
        text=True,
        check=False,
    )


def mock_command(tmp_path: Path, name: str, exit_code: int = 0) -> tuple[Path, Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    log_file = tmp_path / f"{name}.args"
    executable = bin_dir / name
    executable.write_text(
        "#!/bin/sh\n"
        f"printf '%s\\n' \"$@\" > '{log_file}'\n"
        f"exit {exit_code}\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    return bin_dir, log_file


def with_mock_path(bin_dir: Path) -> dict[str, str]:
    return {"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"}


def test_root_task_list_exposes_generic_workflows(task_command: str, task_project: Path) -> None:
    result = run_task(task_command, "--list-all", cwd=task_project)

    assert result.returncode == 0, result.stdout + result.stderr
    output = result.stdout
    for task_name in (
        "dev:up",
        "build",
        "test",
        "lint",
        "deploy:dev",
        "deploy:staging",
        "deploy:prod",
        "infra:plan",
        "infra:apply",
        "docs",
        "docs-docker",
    ):
        assert task_name in output
    assert "docs:deploy" not in output


def test_gitflow_task_list_is_project_agnostic(task_command: str, task_project: Path) -> None:
    result = run_task(task_command, "-t", "Taskfile.gitflow.yml", "--list-all", cwd=task_project)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "feature:start" in result.stdout
    assert "release:start" in result.stdout
    assert "hotfix:start" in result.stdout
    assert "docs:deploy" not in result.stdout


@pytest.mark.parametrize(
    "task_name",
    (
        "dev",
        "dev:down",
        "dev:logs",
        "dev:status",
        "build",
        "test",
        "lint",
        "deploy:dev",
        "deploy:staging",
        "deploy:prod",
        "rollback",
        "infra:plan",
        "infra:apply",
    ),
)
def test_unconfigured_workflows_fail_with_actionable_message(
    task_command: str, task_project: Path, task_name: str
) -> None:
    result = run_task(task_command, task_name, cwd=task_project)

    assert result.returncode != 0
    output = result.stdout + result.stderr
    assert "is not configured for this project" in output
    assert "Add the project-specific commands" in output


def test_check_uses_mocked_precommit(task_command: str, task_project: Path, tmp_path: Path) -> None:
    bin_dir, log_file = mock_command(tmp_path, "pre-commit")

    result = run_task(task_command, "check", cwd=task_project, env=with_mock_path(bin_dir))

    assert result.returncode == 0, result.stdout + result.stderr
    assert log_file.read_text(encoding="utf-8").splitlines() == ["run", "--all-files"]


@pytest.mark.parametrize("task_name, expected_action", (("docs-docker", "up"), ("docs-docker:down", "down")))
def test_documentation_server_tasks_use_mocked_docker(
    task_command: str, task_project: Path, tmp_path: Path, task_name: str, expected_action: str
) -> None:
    bin_dir, log_file = mock_command(tmp_path, "docker")

    result = run_task(task_command, task_name, cwd=task_project, env=with_mock_path(bin_dir))

    assert result.returncode == 0, result.stdout + result.stderr
    assert log_file.read_text(encoding="utf-8").splitlines() == [
        "compose",
        "-f",
        "docker-compose.mkdocs.yml",
        expected_action,
    ] + ([] if expected_action == "down" else ["-d"])


def test_info_reports_template_context(task_command: str, task_project: Path) -> None:
    result = run_task(task_command, "info", cwd=task_project)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Project -> my-project" in result.stdout
    assert "Environment -> dev" in result.stdout
    assert "Docs server -> http://0.0.0.0:8030/" in result.stdout


def materialize_taskfiles(project: Path) -> None:
    project.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "Taskfile.yml", project / "Taskfile.yml")
    shutil.copy(ROOT / "Taskfile.gitflow.yml", project / "Taskfile.gitflow.yml")


@pytest.fixture
def task_project(tmp_path: Path) -> Path:
    project = tmp_path / "task-project"
    materialize_taskfiles(project)
    return project


def git(project: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=project,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def create_git_project(tmp_path: Path, with_remote: bool = False) -> tuple[Path, Path | None]:
    project = tmp_path / "project"
    materialize_taskfiles(project)
    git(project, "init", "-b", "main")
    git(project, "config", "user.name", "Taskfile Tests")
    git(project, "config", "user.email", "taskfile-tests@example.invalid")
    (project / "README.md").write_text("# Test project\n", encoding="utf-8")
    git(project, "add", ".")
    git(project, "commit", "-m", "Initial commit")

    remote: Path | None = None
    if with_remote:
        remote = tmp_path / "origin.git"
        subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True, text=True)
        git(project, "remote", "add", "origin", str(remote))
    return project, remote


def test_root_status_and_info_work_in_a_real_project(task_command: str, tmp_path: Path) -> None:
    project, _ = create_git_project(tmp_path)

    status = run_task(task_command, "status", cwd=project)
    info = run_task(task_command, "info", cwd=project)

    assert status.returncode == 0, status.stdout + status.stderr
    assert "## main" in status.stdout
    assert info.returncode == 0, info.stdout + info.stderr
    assert "Project -> my-project" in info.stdout


def test_gitflow_init_and_feature_start_work_against_local_remote(
    task_command: str, tmp_path: Path
) -> None:
    project, remote = create_git_project(tmp_path, with_remote=True)
    assert remote is not None
    assert git(project, "remote", "get-url", "origin") == str(remote)
    init = run_task(task_command, "-t", "Taskfile.gitflow.yml", "init", cwd=project)
    assert init.returncode == 0, init.stdout + init.stderr
    assert "main" in git(project, "branch", "--format", "%(refname:short)")
    assert "develop" in git(project, "branch", "--format", "%(refname:short)"), init.stdout + init.stderr
    assert git(project, "config", "gitflow.branch.master") == "main"
    assert git(project, "config", "gitflow.branch.develop") == "develop"
    rerun = run_task(task_command, "-t", "Taskfile.gitflow.yml", "init", cwd=project)
    assert rerun.returncode == 0, rerun.stdout + rerun.stderr


    feature = run_task(
        task_command,
        "-t",
        "Taskfile.gitflow.yml",
        "feature:start",
        "name=real-flow",
        cwd=project,
    )
    assert feature.returncode == 0, feature.stdout + feature.stderr
    assert "feature/real-flow" in git(project, "branch", "--format", "%(refname:short)")


def test_gitflow_commit_creates_a_real_commit(task_command: str, tmp_path: Path) -> None:
    project, _ = create_git_project(tmp_path)
    (project / "change.txt").write_text("real task execution\n", encoding="utf-8")

    result = run_task(
        task_command,
        "commit",
        "msg=Taskfile-e2e-commit",
        cwd=project,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert git(project, "log", "-1", "--pretty=%s") == "Taskfile-e2e-commit"
