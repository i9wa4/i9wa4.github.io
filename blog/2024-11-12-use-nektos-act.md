# nektos/act を使ってみた
uma-chan
2024-11-12

GitHub Actions をローカルで実行できる便利な OSS
<https://github.com/nektos/act> を使ってみました。

インストールが難しかったので苦戦した部分もメモを残しておきます。

## 1. 筆者の環境について

- OS: WSL2 Ubuntu 24.04
- Shell: zsh

## 2. バイナリどこ？？

インストール手順 <https://nektosact.com/installation/index.html>
に従って

``` sh
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

を実行したはいいもののインストール先が分からず `which act`
で探しても見つからず。

(2024-11-19 追記: コマンド実行したディレクトリに bin/act
が生成されていました。自分にとっては嬉しくない挙動。)

続いて GitHub CLI extension
としてのインストール方法が簡単そうに見えました。

``` sh
gh extension install https://github.com/nektos/gh-act
```

ただ、 GitHub CLI extension
ってなに？そもそもその仕様を知る必要性を感じなかったためスルー。

仕方がないのでソースコードからビルドすることに。

``` sh
git clone https://github.com/nektos/act.git
cd act/
make build

# 因みに私の環境では以下コマンドでクローンしてます。
# ghq get -p nekotos/act
```

ビルド後 `./dist/local/act`
なるバイナリが生成されたためインストール完了。

面倒なので PATH は通してませんがよい子は通しておきましょう。

## 3. 動作確認

`https://github.com/i9wa4/gha-sandbox` のうち
`.github/workflows/4.6.actionlint.yml` を実行してみます。

``` sh
$ ~/src/github.com/nektos/act/dist/local/act workflow_dispatch -W '.github/workflows/4.6.actionlint.yml'
INFO[0000] Using docker host 'unix:///var/run/docker.sock', and daemon socket 'unix:///var/run/docker.sock'
[4.6. Linting GitHub Actions/lint] 🚀  Start image=catthehacker/ubuntu:act-latest
[4.6. Linting GitHub Actions/lint]   🐳  docker pull image=catthehacker/ubuntu:act-latest platform= username= forcePull=true
[4.6. Linting GitHub Actions/lint]   🐳  docker create image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[] network="host"
[4.6. Linting GitHub Actions/lint]   🐳  docker run image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[] network="host"
[4.6. Linting GitHub Actions/lint]   🐳  docker exec cmd=[node --no-warnings -e console.log(process.execPath)] user= workdir=
[4.6. Linting GitHub Actions/lint] ⭐ Run Main actions/checkout@v4
[4.6. Linting GitHub Actions/lint]   🐳  docker cp src=/home/i9wa4/src/github.com/i9wa4/gha-sandbox/. dst=/home/i9wa4/src/github.com/i9wa4/gha-sandbox
[4.6. Linting GitHub Actions/lint]   ✅  Success - Main actions/checkout@v4
[4.6. Linting GitHub Actions/lint] ⭐ Run Main docker run --rm -v "$(pwd):$(pwd)" -w "$(pwd)" rhysd/actionlint:latest
[4.6. Linting GitHub Actions/lint]   🐳  docker exec cmd=[bash --noprofile --norc -e -o pipefail /var/run/act/workflow/1.sh] user= workdir=
| Unable to find image 'rhysd/actionlint:latest' locally
| latest: Pulling from rhysd/actionlint
43c4264eed91: Pull complete
9ff7a0d1399a: Pull complete
efbbf3bc777d: Pull complete
290bb4d6a286: Pull complete
Digest: sha256:82244e1db1c60d82c7792180a48dd0bcb838370bb589d53ff132503fc9485868
| Status: Downloaded newer image for rhysd/actionlint:latest
[4.6. Linting GitHub Actions/lint]   ✅  Success - Main docker run --rm -v "$(pwd):$(pwd)" -w "$(pwd)" rhysd/actionlint:latest
[4.6. Linting GitHub Actions/lint] Cleaning up container for job lint
[4.6. Linting GitHub Actions/lint] 🏁  Job succeeded

INFO    ️ 📣 A newer version of 'act' is available - consider ugrading to 0.2.69.
```

うまく動いてくれました。

## 4. \[2024-12-05 追記\] Mac でエラーが出た場合

以下の記事が参考になりました。

[WSL2でDocker buildをすると止まる問題(“docker-credential-desktop.exe”:
executable file not found in \$PATH, out: \`\`) \#Docker -
Qiita](https://qiita.com/rasuk/items/a36b29b8c79d02fc551a)
