# TagMark

First of all, thanks for taking your time to contribute and help make our project even better than it is today! The following is a set of guidelines for contributing to TagMark. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Guides

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
  * `modify`: any modifications
    * `modify.fix`: bug fix
    * `modify.perf`: code change that improves performance
    * `modify.style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)
    * `modify.refactor`: code change that neither fixes a bug nor adds a feature
  * `revert`: revert some existing commits
  * `del`: remove
  * `release`: Commit a release for a conventional changelog project

The subject contains a succinct description of the change, like Update code highlighting in README.md.

* No dot (.) at the end.
* Use the imperative, present tense: "change" not "changed" nor "changes".
