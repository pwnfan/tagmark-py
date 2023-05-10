# TagMark

First of all, thanks for taking your time to contribute and help make our project even better than it is today! The following is a set of guidelines for contributing to TagMark. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Guides

### Setup Development Environment

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

**Step 4** install tagmark dependencies

```bash
(testvenv) ➜  cd tagmark
(testvenv) ➜  tagmark git:(dev) ✗ poetry install
```

**Step 5** if your IDE is vscode, here are the recommended settings

`.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false,
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

`.vscode/settings.json`

```json
{
    "python.formatting.provider": "black",
    "python.testing.pytestArgs": ["tests"],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
}
```

**Step 6** create a PAT and store it into the `.env` file in your local tagmark source dir, the details has been refered in [README > Installation > Step 4](../README.md#Installation)

### Build

in the root directory of tagmark, run:

```bash
poetry build
```

### Run Tests

in the root directory of this project run

```bash
# run test
poetry run pytest -v --cov=tagmark tests/
```

### Commit Messages Rules

commit message format: `{scope}>{action}: msg`

* `{scope}`:
  * `infra`: infrastructure, fundamental things
    * `infra.build`: build system or external dependencies(libraries/modules/packages, etc.)
    * `infra.ci`: CI configuration files and scripts
    * `infra.misc`: miscellaneous things or other things
      * .gitignore
      * .github
      * etc
  * `code`: code of TagMark
    * `code.core`: main core code of TagMark in `core` folder
    * `code.tool`: tool/plugin of TagMark in `tool` folder
    * `code.tests`: testing code of TagMark in `tests` folder
    * `code.misc`: miscellaneous things or other things
    * `code.data`: any data used by code
  * `data`
    * any data not userd by code
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
    * `modify.misc`: miscellaneous things or other things
      * comment
  * `revert`: revert any existing commits
  * `del`: remove
  * `release`: Commit a release for a conventional changelog project

The subject contains a succinct description of the change, like Update code highlighting in README.md.

* No dot (.) at the end.
* Use the imperative, present tense: "change" not "changed" nor "changes".
