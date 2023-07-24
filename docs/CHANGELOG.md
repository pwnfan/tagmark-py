# Changelog

Order: The higher up, the newer.

## v0.3.0

* 19abf55 code.core>modify.style: lint
* a6c3f53 infra.misc>modify.fix: ignore E203 in flake8, see https://github.com/psf/black/issues/315 for details
* d83374d infra.misc>modify.fix: add config to skip not implemented code in coverage test
* 60fa94f docs>modify.fix: fix doc according to makefile changes
* e7f25a5 infra.misc>new: add missing term for cov report into `make test`
* 7f0c1ee infra.misc>new: add python cache file/dir into `make clean`
* 25febb3 infra.misc>new: add test file/dir into `make clean`
* c3af867 infra.misc>modify.fix: fix gitignore
* 9149248 docs>modify.refactor: collect all docs into one folder
* 8fd6520 code.misc>modify.misc: fix word spelling of variable
* 90a5765 infra.build>new: add new vsc extension into devcontainer
* c47e6f0 infra.misc>new: add new item into gitignore
* b1ae300 infra.misc>modify.fix: fix gitignore
* 64005ff infra.build>modify.new&&code.core>modify.fix: bump revchatgpt 6.8.6 to fix gpt not working, see https://github.com/acheong08/ChatGPT/issues/1470 for details
* 75ca437 docs>modify.fix: fix content in CONTRIBUTING and CHANGELOG
* 5cbea2a docs>modify.fix: fix changelog order
* a22084c infra.misc>new&&docs>new: add new make command `changelog`
* f50cc81 docs>modify.fix: fix README
* 659fed1 infra.misc>new&&docs>new: add Makefile and related doc
* f0e7091 infra.build>new: add new vsc extension into devcontainer
* a02cc50 code.core>new: update github info only when user specified number of hours has passed since the last update
* d463e49 code.misc>modify.misc: fix word spelling of variable
* e867794 docs>new: add new TODO into README
* 643ebc1 infra.build>new: add devcontainer(vscode)
* 2c0f444 infra.build>modify: update: poetry.lock
* bd791d2 docs>modify.fix: fix errors in README
* bcbdd7f docs>modify.refactor: update data in README
* c8245c3 code.tool>modify.fix: sometimes gpt return empty string with no error, which will unexpectedly overwrite the original prompt string
* 0d8d637 docs>new: add new TODO into README
* d979e52 code.core>new: validate github repo url availability and set TagmarkItem.valid according to the result
* 200777a code.tests>modify.refactor: normalize variable names
* 500db91 docs>modify.new: detailing TODO item in README
* e8925fd docs>new: add new scope and action of git commit mesage rule into CONTRIBUTING.md
* 0b4a9fd docs>new: add new setion `demo` into README

## v0.2.0

* e400bc8 infra.build>modify.new: bump requests from 2.28.2 to 2.31.0 to fix security vul reported by github dependabot
* 9d8c6d9 docs>new: add new content into README
* f780edd code.misc>modify.misc: fix word spelling of help msg in convert sub command
* cb7b733 code.tool>modify.new: add output file log info into `convert`subcommand
* cac1bda code.misc>new: add sub command "autotagdef"
* e4e06b0 code.misc>modify.misc: add comment to `checktag` sub command code
* 7fc0967 docs>new: add new content into README
* a72d352 code.misc>modify.refactor: change defualt value of "checktag -c",  and some help message modify
* 112eeda code.misc>new: add msg to show rate of process in `convert` command
* 5199240 code.misc>new: Tagmark.get_github_repo_infos add condition filter
* c07d897 code.core>modify.style: add support for utf-8 encoding in output jsonlines file
* 54a19bc code.misc>new: add sub command "checktag"
* 9ef2cd6 docs>modify.style: fix white-space in README
* e4e18eb docs>new: add new TODO into README
* f5c4bb6 docs>new: add new section into CONTRIBUTING
* 553f447 docs>new: add new TODO into README
* dca3576 code.tests>new: add test case for Tagmark.count_github_url

## v0.1.0

* finished basic features
