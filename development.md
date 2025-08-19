# Development

## Setup

- clone w/ `--recurse-submodules` and remember to update submodules on pull
    - automatically do these w/
        [these Git
        config](https://sichanghe.github.io/notes/programming/git.html#config)
- use [UV](https://docs.astral.sh/uv/) to manage Python dependencies
    (`uv sync --all-packages`, `uv add`)
    - note: some dependency like `nvidia-cuda-runtime-cu12` version for
        Binoculars are unfortunately hardcoded for Exxact; need to change if
        used on other machine
- install `ruff` and `maturin[patchelf]`:

    ```sh
    uv tool install ruff
    uv tool install maturin[patchelf]
    ```

- [install Rust](https://www.rust-lang.org/tools/install)
- register [Pre-commit Hook](https://pre-commit.com/) to run linters and
    formatters automatically before Git commit:

    ```sh
    . .venv/bin/activate
    pre-commit install
    ```

- copy the content of `../conf_template/` to `../` and modify they as
    appropriate.

## Pull request

- run `. static_checks.sh` before making pull request

## Coordination

- to pause scoring tasks, run:
    ```sh
    sh pause_bino_server.sh
    ```
- after done using the GPU, please allow the tasks to resume:
    ```sh
    sh /ssd1/sichanghe/DeGenTWeb/resume_bino_server.sh
    ```

## Restoring PostgreSQL database

- install PostgreSQL 17 & TimescaleDB v2.21.1
- see
    [PgBackRest
    docs](https://pgbackrest.org/user-guide.html#quickstart/perform-restore)
