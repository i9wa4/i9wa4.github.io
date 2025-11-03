# uma-chan's page

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/i9wa4/i9wa4.github.io)

<https://i9wa4.github.io>

## 1. How to preview this page

1. Install venv with uv.

    ```sh
    uv sync --frozen
    ```

1. Preview with Quarto.

    ```sh
    uv run quarto preview
    ```

## 2. How to update uv.lock

1. Update .python-version or pyproject.toml.
1. Execute the following command.

    ```sh
    uv lock --upgrade
    ```
