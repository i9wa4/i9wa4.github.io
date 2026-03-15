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

<div class="social-share"><a href="https://twitter.com/share?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-06-python-venv.html&text=Python%20venv%20%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%83%BB%E6%9B%B4%E6%96%B0%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%97%E3%83%88%E3%81%AE%E4%BE%9B%E9%A4%8A%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="twitter"><i class="bi bi-twitter-x"></i></a><a href="https://bsky.app/intent/compose?text=Python%20venv%20%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%83%BB%E6%9B%B4%E6%96%B0%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%97%E3%83%88%E3%81%AE%E4%BE%9B%E9%A4%8A%20%E2%80%93%20uma-chan%E2%80%99s%20page%20https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-06-python-venv.html" target="_blank" class="bsky"><i class="bi bi-bluesky"></i></a><a href="https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fi9wa4.github.io%2Fblog%2F2025-05-06-python-venv.html&title=Python%20venv%20%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%83%BB%E6%9B%B4%E6%96%B0%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%97%E3%83%88%E3%81%AE%E4%BE%9B%E9%A4%8A%20%E2%80%93%20uma-chan%E2%80%99s%20page" target="_blank" class="linkedin"><i class="bi bi-linkedin"></i></a></div>
