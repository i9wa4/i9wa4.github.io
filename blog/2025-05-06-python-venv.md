# Python venv インストール・更新スクリプトの供養
uma-chan
2025-05-06

## 1. はじめに

uv で venv 仮想環境をメンテナンスすることにしたためこれまで利用していた
venv のインストール・更新スクリプトを供養します。

## 2. スクリプト (Makefile)

実際はこのように Makefile
に書いていましたが、流石に見辛いのでシェルスクリプト版も載せます。

``` Makefile
python-venv:  ## install/update Python venv (e.g. make python-venv VENV_PATH="${PY_VENV_MYENV}" REQUIREMENTS_PATH="${HOME}"/ghq/github.com/i9wa4/dotfiles/etc/requirements-venv-myenv.txt)
    # https://dev.classmethod.jp/articles/change-venv-python-version/
    . $(MF_DOTFILES_DIR)/dot.zshenv \
    && if [ -d "$(VENV_PATH)" ]; then \
      python -m venv "$(VENV_PATH)" --clear; \
    else \
      python -m venv "$(VENV_PATH)"; \
    fi \
    && . "$(VENV_PATH)"/bin/activate \
    && python -m pip config --site set global.trusted-host "pypi.org pypi.python.org files.pythonhosted.org" \
    && python -m pip install --upgrade pip setuptools wheel \
    && [ -r "$(REQUIREMENTS_PATH)" ] && python -m pip install --requirement "$(REQUIREMENTS_PATH)" \
    && python -m pip check \
    && python --version \
    && deactivate
```

## 3. スクリプト (シェルスクリプト)

``` sh
#!/usr/bin/env bash

VENV_PATH="${HOME}"/.venv
REQUIREMENTS_PATH="${HOME}"/requirements.txt

if [ -d "${VENV_PATH}" ]; then
  python -m venv "${VENV_PATH}" --clear;
else
  python -m venv "${VENV_PATH}";
fi

. "${VENV_PATH}"/bin/activate
python -m pip config --site set global.trusted-host "pypi.org pypi.python.org files.pythonhosted.org"
python -m pip install --upgrade pip setuptools wheel
[ -r "${REQUIREMENTS_PATH}" ] && python -m pip install --requirement "${REQUIREMENTS_PATH}"
python -m pip check
python --version
deactivate
```
