# TagMark

- [TagMark](#tagmark)
  - [Guides](#guides)
    - [Development Environment Setup](#development-environment-setup)
      - [1. Setup Python and Poetry](#1-setup-python-and-poetry)
        - [Option 1: Using self-created virtual env](#option-1-using-self-created-virtual-env)
        - [Option 2: Using VSCode + devcontainer](#option-2-using-vscode--devcontainer)
      - [2. Setup GITHUB\_TOKEN](#2-setup-github_token)
      - [3. Install TagMark Dependencies](#3-install-tagmark-dependencies)
        - [Option 1: Using make Command](#option-1-using-make-command)
        - [Option 2: Run Original Command(s)](#option-2-run-original-commands)
      - [4. Linting](#4-linting)
        - [Option 1: Using make Command](#option-1-using-make-command-1)
        - [Option 2: Run Original Command(s)](#option-2-run-original-commands-1)
      - [5. Testing](#5-testing)
        - [Option 1: Using make Command](#option-1-using-make-command-2)
        - [Option 2: Run Original Command(s)](#option-2-run-original-commands-2)
      - [6. Build](#6-build)
        - [Option 1: Using make command](#option-1-using-make-command-3)
        - [Option 2: Run Original Command(s)](#option-2-run-original-commands-3)
      - [7. Clean Up](#7-clean-up)
        - [Option 1: Using make command](#option-1-using-make-command-4)
        - [Option 2: Run Original Command(s)](#option-2-run-original-commands-4)
      - [8. Generating Changelog](#8-generating-changelog)
        - [Option 1: Using make command](#option-1-using-make-command-5)
        - [Option 2: Run Original Command(s)](#option-2-run-original-commands-5)
    - [Commit Messages Rules](#commit-messages-rules)
    - [Code Style](#code-style)

First of all, thanks for taking your time to contribute and help make our project even better than it is today! The following is a set of guidelines for contributing to TagMark. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Guides

### Development Environment Setup

First please enter the root directory of `tagmark`.

#### 1. Setup Python and Poetry

##### Option 1: Using self-created virtual env

**Step 1** create you and enter virtual environment:

here we take mamba(conda) as example:

```bash
 ➜ mamba create -n testvenv python=3.11
 ➜ mamba activate testvenv
```

**Step 2** install poetry

```bash
(testvenv) ➜ pip install poetry
```

**Step 3** fork and clone the tagmark repo

**Step 4** if your IDE is vscode, here are the recommended settings

`.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Module",
            "type": "python",
            "request": "launch",
            "cwd": "${workspaceRoot}",
            "module": "tagmark.cli",
            "justMyCode": false,
            "args": [
                // args for debug, change according to your needs 
                "convert",
                "-i",
                "data/tagmark_ui_data.jsonl",
                "-f",
                "tagmark_jsonlines",
                "-o",
                "data/new_tagmark_ui_data.jsonl"
            ]
        }
    ]
}
```

`.vscode/settings.json`

```json
{
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter"
    },
    "python.formatting.provider": "none",
}
```

##### Option 2: Using VSCode + devcontainer

**Step 1** run Docker daemon

**Step 2** Build devcontainer image and start container:

in a new VSCode win, press Ctrl+Shift+P(windows) / Command+Shift+P(MacOS) to open `Command Palette` and select `Dev container: Clone Repository in Container Volume...`, you may be required to enter these/choose things:
  * `git repo url``: <https://github.com/pwnfan/tagmark.git>
  * Python version: you should select version >= 3.11
  * Linux Distribution: I selected the first one(an alias of a specified version of ubuntu), but I did not test the others. You can try what you like.

after a while the image will be built and the container will be run, the VSCode windows will be reloaded and the git repo will show up.

#### 2. Setup GITHUB_TOKEN

create a PAT and store it into the `.env` file in your local tagmark source dir, the details has been referred in [README > Installation > Step 4](README.md#Installation)


#### 3. Install TagMark Dependencies

##### Option 1: Using make Command


```bash
make install
```

##### Option 2: Run Original Command(s)


```bash
poetry install
```

#### 4. Linting

##### Option 1: Using make Command

```bash
make lint
```

##### Option 2: Run Original Command(s)


```bash
black .
isort --profile black .
flake8 --ignore=E501,W503 .
```

#### 5. Testing

##### Option 1: Using make Command

```bash
make test
```

##### Option 2: Run Original Command(s)


```bash
poetry run pytest -v --cov=tagmark tests/
```

#### 6. Build

##### Option 1: Using make command

```bash
make build
```

##### Option 2: Run Original Command(s)

```bash
poetry build
```

#### 7. Clean Up

##### Option 1: Using make command

```bash
make clean
```

##### Option 2: Run Original Command(s)


```bash
rm -rf dist
rm -rf .coverage
```

#### 8. Generating Changelog

##### Option 1: Using make command

```bash
make changelog V_OLD=v0.1.0 V_NEW=v0.2.0 OUT_FILE=changelog.txt
```

* `V_OLD`: an older(starting) Git commit version number, its optional values are:
  * Git commit hash
  * Git tag
* `V_NEW`: a newer(ending) Git commit version number, its optional values are:
  * Git commit hash
  * Git tag
  * HEAD, HEAD^, HEAD~3, etc.
* `OUT_FILE`: the path of the output file

##### Option 2: Run Original Command(s)

```bash
git log V_OLD..V_NEW --oneline --abbrev-commit --pretty="* %h %s" > OUT_FILE;
```

the meaning of the arguments are the same as those in [Option 1: Using make command](#option-1-using-make-command-5).

example:

```bash
git log v0.1.0..v0.2.0 --oneline --abbrev-commit --pretty="* %h %s" > changelog.txt
```

### Commit Messages Rules

commit message format: `{scope}>{action}: msg`

* `{scope}`:
  * `infra`: infrastructure, fundamental things
    * `infra.build`: build system
    * `infra.ci`: CI configuration files and scripts
    * `infra.misc`: miscellaneous things or other things
      * .gitignore
      * .github
      * Makefile
      * etc
  * `code`: code of TagMark
    * `code.dep`: (external) dependencies(libraries/modules/packages, etc.)
    * `code.core`: main core code of TagMark in `core` folder
    * `code.tool`: tool/plugin of TagMark in `tool` folder
    * `code.tests`: testing code of TagMark in `tests` folder
    * `code.misc`: miscellaneous things or other things
    * `code.data`: any data used by code
  * `data`
    * any data not used by code
    * the final output/result of the code execution
    * etc
  * `docs`: documentation
  * `proj`: this project, often used in combination with the `release` action
* `{action}`:
  * `new`
    * add new file(s) to a scope
    * add new feature to existing file(s)
    * add new content to existing document(s)
  * `modify`: any modifications for existing files
    * `modify.fix`: bug fix
    * `modify.perf`: code change that improves performance
    * `modify.style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, naming, etc.)
    * `modify.refactor`: code refactor which not relates to fix, perf and style
    * `modify.update`: update an external dependencies(libraries/modules/packages, etc.)
    * `modify.misc`: miscellaneous things or other things
      * comment
  * `revert`: revert any existing commits
  * `del`: remove
  * `release`: Commit a release for a conventional changelog project

The subject contains a succinct description of the change, like Update code highlighting in README.md.

* No dot (.) at the end.
* Use the imperative, present tense: "change" not "changed" nor "changes".

### Code Style

please run the linter command in [4. Linting](#4-linting) to format your code before pushing your pull request.

The Linting commands will also be run in the CI progress auto triggered by Github Actions to check the style of your code when you push your pull request to `dev` branch. If the check failed your pull request is not able to be merged.
