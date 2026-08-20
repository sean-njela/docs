<div align="center">

  <!-- Icon (optional, uncomment if needed) -->
  <!--
  <p>
    <img src="https://logo.svgcdn.com/d/kubernetes-plain-wordmark.svg" alt="Kubernetes" height="95" />
  </p>
  -->

  <h1>Project Title</h1>

  <p>
    Short description of the project. What it does, what problem it solves, or what it demonstrates.
  </p>

  <p>
    <a href="https://github.com/your-org/your-repo/graphs/contributors">
      <img src="https://img.shields.io/github/contributors/your-org/your-repo" alt="contributors" />
    </a>
    <a href="">
      <img src="https://img.shields.io/github/last-commit/your-org/your-repo" alt="last update" />
    </a>
    <a href="https://github.com/your-org/your-repo/network/members">
      <img src="https://img.shields.io/github/forks/your-org/your-repo" alt="forks" />
    </a>
    <a href="https://github.com/your-org/your-repo/stargazers">
      <img src="https://img.shields.io/github/stars/your-org/your-repo" alt="stars" />
    </a>
    <a href="https://github.com/your-org/your-repo/issues/">
      <img src="https://img.shields.io/github/issues/your-org/your-repo" alt="open issues" />
    </a>
    <a href="https://github.com/your-org/your-repo/blob/master/LICENSE">
      <img src="https://img.shields.io/github/license/your-org/your-repo.svg" alt="license" />
    </a>
  </p>
</div>

## Screenshots

<details>
  <summary>Click to expand</summary>
  <!-- Example (uncomment if needed) -->
  <div align="center">
    <img src="assets/screenshot1.png" alt="screenshot1" width="800" />
    <img src="assets/screenshot2.png" alt="screenshot2" width="800" />
  </div>
</details>

## Tech Stack

> List of tools used in the project

![mise](https://img.shields.io/badge/mise-managed-blue)
![Taskfile](https://img.shields.io/badge/Taskfile-3.44.1-green)
![gitflow-next](https://img.shields.io/badge/git--flow--next-2.0.0-green)
![uv](https://img.shields.io/badge/uv-0.8.14-green)
![precommit](https://img.shields.io/badge/precommit-4.3.0-green)

## Prerequisites

This project uses `mise.toml` and `mise.lock` for a reproducible development
environment. Install Git and mise first. Docker is only required for the
optional containerized documentation server.

Clone the repository and enter it:

```bash
git clone ...
cd ...
```

Install the pinned project tools and prepare the Python environment:

```bash
mise install
task setup
```

The project uses the tools declared in `mise.toml`. `mockoon` is not included
because mise does not provide a matching backend; install it separately only
if your project needs it.

## Quick Start

```bash
mise install
task setup
task status   # check if anything is running
task dev      # start development stack
task cleanup-dev
```


## Documentation

For full documentation, setup instructions, and architecture details, visit the [docs](docs/index.md) directory or run locally with:

```bash
task docs
```

Then open: [http://127.0.0.1:8030/]()

## Tasks (Automation)

> [!IMPORTANT]
> This project keeps environment setup in mise and project automation in `Taskfile.yml`.

The `Taskfile.gitflow.yml` provides a structured Git workflow using Git Flow. This helps in managing features, releases, and hotfixes in a standardized way. Running these tasks is the same as running any other task. Using gitflow is optional. If you do not want the gitflow tasks, you can remove the `Taskfile.gitflow.yml` file and unlink it from the `Taskfile.yml` file (remove the `includes` section). If you cannot find the section use CTRL + F to search for `Taskfile.gitflow.yml`.

To see all tasks:

```bash
task --list-all
```

## Contributing

<a href="https://github.com/sean-njela/your-repo/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=sean-njela/your-repo" />
</a>

> Contributions welcome! Open an issue or submit a PR.

## License

Distributed under the MIT License. See `LICENSE` for more info.

## Contact

* [LinkedIn](https://linkedin.com/in/sean-njela)
* [Twitter/X](https://x.com/devopssean)
* [seannjela@outlook.com](mailto:seannjela@outlook.com)
* [About Me](docs/4-about/0-about.md)
