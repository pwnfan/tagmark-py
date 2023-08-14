# Changelog

Order: The higher up, the newer.

## v1.0.0

* fb2a1bd Merge pull request #29 from pwnfan/dev
* b94822b docs>new&&docs>modify.fix: add new and modify old content in README
* 4883ef1 infra.misc>modify.refactor: modify project description in pyproject.toml
* add0f84 infra.ci>new: add release action
* 1d0cc36 infra.misc>new: add FUNDING
* 71c4bd6 infra.ci>modify.new: add step to upload coverage reports to codecov, and add trigger condition `on push`
* db9e718 code.core>modify.fix: correct the grammatical errors in the help message
* 94e1de6 Merge pull request #28 from pwnfan/dev
* 8a6f9d0 code.core>modify.refactor: remove space to generate  more compacted json-lines file
* 10823a8 code.core>modify.fix: fix bug when working with ui when url_base is a relative url or a sub directory
* c1ae689 code.core>modify.fix: fix parameter name error
* cc7904d code.core>modify.refactor: modify CLI log msg
* f0f9664 code.core>modify.refactor: order the subcommands in the help msg
* c431018 code.core>modify.fix: fix the variable name and description mistakes saying that "tagmark jsonlines data" as "tagmark json data"
* 46e097c code.core>modify.refactor: detail the error msg when missing cookie for `export` subcommand
* a61e7e3 code.core>new: add new type `diigo_web_exported` into `convert -f`
* e0ee4a5 code.core>modify.fix>fix the default value of `export -o`
* 4bd1333 code.tests>modify.style: lint code
* 37e4232 infra.ci>modify.fix> fix ci lint error for PEP8 E203, see infra.misc>modify.fix: ignore E203 in flake8, see https://github.com/psf/black/issues/315 for details
* 698bfda code.core>modify.refactor: rename classes
* dac87bb code.core>new: add `export` subcommand and diigo web exporter
* e04e2e0 code.tests>modify.fix: fix leaving test temp file unremoved
* fa07dd1 code.core>modify.refactor: rename classes and module aliases
* 53123e8 code.core>modify.fix: fix the default value of `covert -o` option
* 7b95e7d infra.misc>modify.refactor: simplify arg name of `make changelog`
* 8cc410b code.core>modify.refactor: rename exception names in cli.py
* 41e7b74 code.core>modify.refactor: add log to show no definition tags into `autotagdef` subcommand
* 602f7e2 code.core>modify.style: lint code
* c1910ef code.core>modify.refactor: add error log containing line string into `maketagdoc` subcommand
* b7c9c08 code.tests>modify.refactor: modify test data
* 519ffe1 code.core>modify.fix: `maketagdoc` wrong count when template exppression is `{{f+c:sec AND article AND NOT chinese AND NOT japanese AND NOT korean}}`
* c4a5d22 code.core>modify.fix: `maketagdoc` `f:` template expression missed brackets
* 7ea8e23 code.core>modify.fix: `maketagdoc` generated url is not encoded
* b48b99a code.core>new: `checktag` add check for duplicated  tag formatted names
* 9b09f0f code.tests>modify.refactor: change  common fixture function name
* 6d851f8 code.core>modify.refactor: change subcommand function name
* 0bbdd0d code.misc>new: add sub command "maketagdoc"
* 1a1b597 infra.misc>modify.fix: suppress the subsequent echo  command when the first command failed
* 0420b6d code.core>modify.refactor: change variable name
* 240c36c code.core>new: add new class `TagmarkFilter`
* d483925 code.core>modify.refactor: add missing type hint
* 2d0baad docs>modify.refactor: move LICENSE into `docs` folder
* 651d309 code.core>modify.fix: fix `checktag` subcommand error
* 94a6f17 code.core>modify.fix: fix `tagmark_cli -h` not work
* 17d271b core.misc>modify.refactor: change the data structure of tag json file, and making relate change to code: 1. change the way to generating gpt prompt 2. detail tag with several properties to make preparation for adding the `cheatsheet` subcommand
* 79da854 docs>new: add new TODO into README
* b200ae5 infra.misc>modify.fix: add `changelog` into `.PHONY` in Makefile

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
