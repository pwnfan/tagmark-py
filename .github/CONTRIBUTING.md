# TagMark

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

create a PAT and store it into the `.env` file in your local tagmark source dir, the details has been referred in [README > Installation > Step 4](../README.md#Installation)


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

### Commit Messages Rules

commit message format: `{scope}>{action}: msg`

* `{scope}`:
  * `infra`: infrastructure, fundamental things
    * `infra.build`: build system
    * `infra.ci`: CI configuration files and scripts
    * `infra.misc`: miscellaneous things or other things
      * .gitignore
      * .github
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
