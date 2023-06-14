# tagmark (Python)

- [tagmark (Python)](#tagmark-python)
  - [Features And Demo](#features-and-demo)
  - [What is TagMark](#what-is-tagmark)
  - [Installation](#installation)
  - [Usage](#usage)
    - [sub command: convert](#sub-command-convert)
      - [Usage Examples](#usage-examples)
      - [Core Options Explantation and Design Details](#core-options-explantation-and-design-details)
    - [sub command: checktag](#sub-command-checktag)
      - [Usage Examples](#usage-examples-1)
    - [sub command: autotagdef](#sub-command-autotagdef)
      - [Usage Examples](#usage-examples-2)
    - [Condition File Details](#condition-file-details)
  - [Acknowledgments](#acknowledgments)
  - [Contributing](#contributing)
  - [TODO](#todo)

## Features And Demo

Here is a page as the demo of TagMark usage, which is all my bookmarks integrated in my blog:

<https://www.pwn.fan/tagmark/>

Fetures of the page:

- Substantial tag based bookmarks
  - 1400+ tagged bookmarks, which contain contents below:
    - cybersecurity
      - red team
      - blue team
      - etc
    - software development, devops, devsecops
    - blogs of a person, enterprise, team or organization which refer to the above topics
    - etc
  - 1000+ curated Github Repos
  - 600+ tags with detailed tag definitions
- Full featured tags
  - tag definitions (show/hide definition by left click on tags)
  - tag overview with counts
  - color difference depending on counts
- Simple but powerful header filter for each column
  - thick client: static, pure frontend and js based, so it's fast responding
  - simple and useful fitler grammer
  - quickly input tag name into filter by just a right click
  - press CTRL/CMD with left click in any filter input to call out multiple language document (English/Japanese/Chinses)
- Supporting for URL GET paramaters based filtering
  - static, pure frontend and js based
  - easy for sharing
- Columns related things
  - detailed Github repository information
  - suppressible columns

see [the gif demos on my blog](https://www.pwn.fan/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#what-is-tagmark).

I'm glad to share all my bookmarks with you. Welcome to help me enhance this /tagmark page in my blog by:

- [Contributing and Sharing Your Great Bookmark(s)](https://github.com/pwnfan/pwnfan.github.io/issues/1#issue-1729293100)
- [Reporting Improper Tag Definitions](https://github.com/pwnfan/pwnfan.github.io/issues/2#issue-1729295366)
- [Reporting Improper Tag For Bookmarks](https://github.com/pwnfan/pwnfan.github.io/issues/3#issue-1729507987)

## What is TagMark

TagMark is a tag based browser bookmark solution for developers.

I have written a blog post [TagMark: Maybe a Better Browser Bookmark Solution](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/) to introduce TagMark in details with a toc below:

- [What Is TagMark](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#what-is-tagmark)
- [What Is A "browser bookmark solution"](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#what-is-a-browser-bookmark-solution)
- [Why Do We Need Tags For Bookmarks](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#why-we-need-tags-for-bookmarks)
- [Why Not Diigo Bookmark Manager (Diigo My Library))](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#why-not-diigo-bookmark-manager-diigo-my-library)
- [TagMark's solution: How to build your own TagMark](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#tagmarks-solution-how-to-build-your-own-tagmark)
  - [Generating Your TagMark Data](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#generating-your-tagmark-data)
  - [Defining Your Tags With The Help Of ChatGPT](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#defining-your-tags-with-the-help-of-chatgpt)
  - [Periodically Upading Your TagMark Data and Tag Definitions](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#periodically-upading-your-tagmark-data-and-tag-definitions)
- [Advanced usages](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#advanced-usages)
- [FAQ](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#faq)

I recommend you read the blog first, to save time you can only read the [What is TagMark](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#what-is-tagmark) section and [TagMark's solution: How to build your own TagMark](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#tagmarks-solution-how-to-build-your-own-tagmark) section.

This repository `tagmark`(Python) is a part of the TagMark solution, and this doc is also only for the `tagmark`(Python) part.

## Installation

Requirements: Python>=3.11

**Step 1** install Python, we recommend installing in a virtual environment(pyenv/conda)

**Step 2** download the `tagmark-x.y.z-py3-none-any.whl` or `tagmark-x.y.z.tar.gz` package from the [Release Page](https://github.com/pwnfan/tagmark/releases)

**Step 3** install with pip:

```bash
pip install tagmark-x.y.z-py3-none-any.whl
```

or

```bash
pip install tagmark-x.y.z.tar.gz
```

**Step 4** Setup Github PAT (optional)

if you don't have any Github Repo Bookmarks, this step can be skipped.

1. [create a github personal access token(PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
   `tagmark` requires PAT to access the Github API to get the repo info(stars, forks etc.) when a bookmark url is a Github repo url. The default settings to the PAT is recommended, which has no any priviledge for any action to any of your repos or settings.

2. create `.env` file containing the PAT. `.env` can be created in any directory you want:
    ```bash
    # create a file `.env` containing github aceess token
    echo "GITHUB_TOKEN=github_pat_XXX" > .env
    ```

**Step 5** run tagmark

command line options:

```bash
(testvenv) ➜ tagmark_cli --help
Usage: tagmark_cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  autotagdef  get tag definition automatically by ChatGPT
  checktag    check every tag has a definition
  convert     convert other bookmark formats into Tagmark format(json-lines)
```

## Usage

### sub command: convert

  </summary>

`convert` helps to convert other bookmark formats(diigo_chrome/tagmark_jsonlines) into Tagmark data format(json-lines).

```bash
(py311) ➜  tagmark_cli convert --help                                                            
Usage: tagmark_cli convert [OPTIONS]

  convert other bookmark formats into Tagmark format(json-lines)

Options:
  -i, --input-file-path FILE      input file path
  -f, --format [diigo_chrome|tagmark_jsonlines]
                                  format of the input file  [default:
                                  diigo_chrome]
  -o, --output-file-path FILE     output file path  [default:
                                  tagmark_ui_data.jsonl]
  -k, --keep_empty_keys BOOLEAN   whether keep keys with empty values
                                  [default: False]
  -c, --condition-json-path FILE  json file containing the condition for
                                  fitlering TagmarkItem  [default: /Users/pwn
                                  an/Desktop/Projects/tagmark/tagmark/conditi
                                  on_example.json]
  -b, --is-ban-condition BOOLEAN  If set to True, a TagmarkItem hits the
                                  `condition` will be banned, or it will be
                                  remained  [default: True]
  -t, --github_token TEXT         the GITHUB_TOKEN to access Github API,
                                  default will read from the .env file of the
                                  root dir of this project
  --help                          Show this message and exit.
```

Please refer to section [Core Options Explantation and Design Details](#core-options-explantation-and-design-details) for details of the options.

Please refer to [TagMark: Maybe a Better Browser Bookmark Solution > TagMark's solution: How to build your own TagMark > Generating Your TagMark Data](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#generating-your-tagmark-data) for usage scenarios of `convert` sub command.

#### Usage Examples

```bash
# convert from Diigo output(Chrome format) into TagMark json-lines format file tagmark_ui_data.jsonl
(py311) ➜  tagmark_cli convert -i data/16400249_chrome_2023_04_24_0a65e.html -f diigo_chrome

# actually not for convertion, but for refreshing Github repo information in the file tagmark_ui_data.jsonl
# and output into a new file new_tagmark_ui_data.jsonl
(py311) ➜  tagmark_cli convert -i data/tagmark_ui_data.jsonl -f tagmark_jsonlines -o new_tagmark_ui_data.jsonl
```

#### Core Options Explantation and Design Details

- `-f`: the input file [default: diigo_chrome]
  - `diigo_chrome`: the Chrome format bookmarks exported from Diigo library, see [my blog](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#tagmarks-solution) for details
  - `tagmark_jsonlines`: indicate the input file is a tagmark format json-lines file, which is the output file of the `-o` option of this script. This may be confused, but it's not useless, the purpose of using a `-o` output file as the `-i` input file in a next run, is to refresh the Github info(Starts, Forks, Last Commit, etc) of the bookmarks who are Github repos.

- `-k`: whether keep keys with empty values [default: False]. This is to opitmize the output file size by removing the keys with empty values.

- `-c` and `-b`:

the whole workflow of tagmark:

```bash
                                            ┌──────────────┐
                                            │      -b      │
                                            │  This is a   │
                                            │ban-condition?│
                    ┌────────────┐          └───────┬──────┘
                    │TagmarkItem │                  │
                    │┌───────────┴┐                 ▼
┌───────────┐       └┤TagmarkItem │        ┌────────────────┐       ┌───────────┐
│    -i     │        │┌───────────┴┐──────▶│Filter Condition│──────▶│    -o     │
│Input File │───────▶└┤TagmarkItem │       └────────────────┘       │Output File│
└───────────┘         │ ┌──────────┴─┐              ▲               └───────────┘
                      └─┤TagmarkItem │              │
                        │            │     ┌────────┴───────┐
                        └────────────┘     │       -c       │
                                           │ Condition File │
                                           └────────────────┘
```

`-c` specify a json file containing the condition for fitlering TagmarkItem, the default condition file is `tagmark/condition_example.json`, with content of:

```json
{
    "tags": ["Diigo"],
    "valid": true
}
```

What is a TagmarkItem? Taking a look at the output file format of `-o`, which is a json-lines format file, with one json data in one line. It is the json dump of TagmarkItem object, one line json data looks like:

```json
{
    "url": "https://github.com/jonschlinkert/remarkable",
    "id": 2,
    "valid": true,
    "title": "jonschlinkert/remarkable: Markdown parser, done right. Commonmark support, extensions, syntax plugins, high speed - all in one. Gulp and metalsmith plugins available. Used by Facebook, Docusaurus and many others! Use https://github.com/breakdance/breakdan",
    "tags": ["dev", "frontend", "javascript", "markdown"],
    "is_github_url": true,
    "github_repo_info": {
        "url": "https://github.com/jonschlinkert/remarkable",
        "owner": "jonschlinkert",
        "name": "remarkable",
        "description": "Markdown parser, done right. Commonmark support, extensions, syntax plugins, high speed - all in one. Gulp and metalsmith plugins available. Used by Facebook, Docusaurus and many others! Use https://github.com/breakdance/breakdance for HTML-to-markdown conversion. Use https://github.com/jonschlinkert/markdown-toc to generate a table of contents.",
        "time_created": "2014-09-01T17:57:42Z",
        "time_last_commit": "2023-03-30T05:55:40Z",
        "count_star": 5514,
        "count_fork": 396,
        "count_watcher": 5514,
        "topics": [
            "commonmark",
            "compile",
            "docusaurus",
            "gfm",
            "javascript",
            "jonschlinkert",
            "markdown",
            "markdown-it",
            "markdown-parser",
            "md",
            "node",
            "nodejs",
            "parse",
            "parser",
            "syntax-highlighting"
        ]
    },
    "time_added": "1682907038"
}
```

you can treat this json structure as the data structure of a TagmarkItem, `-c` condition file and `-b` specify a fitler telling tagmark if or not to output a TagmarkItem into the `-o` output file.

for example, if you _**do not**_ need any lines with tag `javascript` _**or**_ `css` to be output in the output file, you should specify your condition file by `-c my_condition.json` with the content below:

```json
{
    "tags": ["javascript", "css"],
}
```

and you need to specify the `-b True (default)` option, which means if a TagmarkItem meets the condition, it will be banned and will not be exported into to output file.

On the contrary, if you only need lines with tag `javascript` _**or**_ `css` to be output into the output file, you need to specify the `-b False` option, which means if a TagmarkItem meets the condition, it will be picked out(not banned) and put into the output file.

Check the [Condition File Details](#condition-file-details) section for more about condition file.

### sub command: checktag


`checktag` helps to verify if every tag in the output file generated by the `-o` parameter of the `convert` sub command has a definition in the tag definition file. This ensures the web UI [tagmark-ui](https://github.com/pwnfan/tagmark-ui) works better.

```bash
(py311) ➜  tagmark_cli checktag --help
Usage: tagmark_cli checktag [OPTIONS]

  check every tag has a definition

Options:
  -t, --tagmark-data-file-path FILE
                                  the tagmark data file path, which may be the
                                  output file generated by the `-o` parameter
                                  of the `convert` sub command
  -d, --tag-definition-file-path FILE
                                  tag definition file path
  -c, --condition-json-path FILE  json file containing the condition for
                                  fitlering TagmarkItem, here only the value
                                  of `tags` field in the file will be used,
                                  and this condition must be a ban condition
                                  [default: /Users/pwnfan/Desktop/Projects/tag
                                  mark/tagmark/condition_example.json]
  -a, --add-no-def-tag BOOLEAN    if set to `True`, a new tags definition file
                                  will be generated, which includes tags in
                                  the old tag definition file, and tags in the
                                  tagmark data file(specified by -t) without a
                                  tag definition. The latter tags are added as
                                  keys with a placeholder value specified by
                                  `-p / --no-def-tag-value-placeholder`
                                  parameter. If set to `False` and any tag
                                  without definition exists, an error will be
                                  raised  [default: True]
  -p, --no-def-tag-value-placeholder TEXT
                                  explained in the `-a` parameter  [default:
                                  !!!NO DEFINITION FOR THIS TAG, PLEASE ADD
                                  HERE!!!]
  --help                          Show this message and exit.
```

Please refer to

- [TagMark: Maybe a Better Browser Bookmark Solution > TagMark's solution: How to build your own TagMark > Defining Your Tags With The Help Of ChatGPT](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#defining-your-tags-with-the-help-of-chatgpt)
- [TagMark: Maybe a Better Browser Bookmark Solution > TagMark's solution: How to build your own TagMark > Periodically Upading Your TagMark Data and Tag Definitions](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#periodically-upading-your-tagmark-data-and-tag-definitions)

for usage scenarios of `checktag` sub command.
#### Usage Examples

```bash
# check every tag in `tagmark_ui_data.jsonl` has a definition in `tag_definitions.json`. If not so a new tag definition file whose name like `new-20230519183413-tag_definitions.json` will be generated, in this file tags already have definition will be added, as well as tags without definition, the latter tags will be added as keys with a placeholder value(default) "!!!NO DEFINITION FOR THIS TAG, PLEASE ADD HERE!!"
tagmark_cli checktag -t tagmark_ui_data.jsonl -d tag_definitions.json -c my-condition.json
```

```bash
# check every tag in `tagmark_ui_data.jsonl` has a definition in `tag_definitions.json`. If not error `tagmark.cli.TagDefinitionMissingError: tags without definition found` will be raise, with the details of the missing definition tags.
tagmark_cli checktag -t tagmark_ui_data.jsonl -d tag_definitions.json -c my-condition.json -a false
```

### sub command: autotagdef

`autotagdef` helps to get tag definition automatically from ChatGPT **based on the prompt given by users.**

```bash
(py311) ➜  tagmark git:(dev) ✗ tagmark_cli autotagdef --help
Usage: tagmark_cli autotagdef [OPTIONS]

  get tag definition automatically by ChatGPT

Options:
  -d, --tag-definition-file-path FILE
                                  tag definition file path
  -f, --gpt-prompt-ending-flag TEXT
                                  the ending flag of the prompt(question) sent
                                  to ChatGPT to get a answer about a tag
                                  definiton  [default: ?]
  -c, --gpt-config-file-path FILE
                                  the config file for invoking ChatGPT API, we
                                  sugguest setting `access_token` in the
                                  config file, see https://github.com/acheong0
                                  8/ChatGPT#--optional-configuration for
                                  details.
  -i, --gpt-conversation-id TEXT  the id of conversation in which to (continue
                                  to) interact with ChatGPT, if set to `None`
                                  a new conversation will be created. See http
                                  s://github.com/acheong08/ChatGPT/wiki/V1#ask
                                  for details.
  -t, --gpt-timeout INTEGER       the timeout that GPT answers one
                                  question(get one tag definition)  [default:
                                  60]
  -p, --no-def-tag-value-placeholder TEXT
                                  explained in the `-a` parameter  [default:
                                  !!!NO DEFINITION FOR THIS TAG, PLEASE ADD
                                  HERE!!!]
  --help                          Show this message and exit.
```

Please refer to

- [TagMark: Maybe a Better Browser Bookmark Solution > TagMark's solution: How to build your own TagMark > Defining Your Tags With The Help Of ChatGPT](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#defining-your-tags-with-the-help-of-chatgpt)
- [TagMark: Maybe a Better Browser Bookmark Solution > TagMark's solution: How to build your own TagMark > Periodically Upading Your TagMark Data and Tag Definitions](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#periodically-upading-your-tagmark-data-and-tag-definitions)

for usage scenarios of `autotagdef` sub command.

#### Usage Examples

```bash
poetry run tagmark_cli autotagdef -d tag_definitions.json -c gpt_config.json -i cca29e06-692e-4a52-84be-c47a7ca524cc
```


```bash
(py311) ➜  tagmark git:(dev) ✗ poetry run tagmark_cli autotagdef -d tag_definitions.json -c gpt_config.json -i cca29e06-692e-4a52-84be-c47a7ca524cc
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 471/471 [00:45<00:00, 10.41it/s]
{"filename": "cli.py", "func_name": "autotagdef", "level": "info", "lineno": 345, "logger": "tagmark.cli", "msg": "new tags definition file has been generated", "new_tags_definition_file": "PosixPath('/Users/pwnfan/Desktop/Projects/tagmark/new-20230522223828-tag_definitions.json')", "process": 82747, "process_name": "MainProcess", "timestamp": "2023-05-22T22:38:28.280672"}
{"auto_tag_make_stats": "AutoTagMakeStats(count_total_tags=471, count_auto_made_success=1, count_auto_made_fail=0, count_no_prompt=0, count_already_defined=470)", "filename": "cli.py", "func_name": "autotagdef", "level": "info", "lineno": 349, "logger": "tagmark.cli", "msg": "statistics", "process": 82747, "process_name": "MainProcess", "timestamp": "2023-05-22T22:38:28.334363"}
```

### Condition File Details

Note that not all keys in TagmarkItem are supported in condition filter files, here is a table for details:

| key              | value type    | supported in condition file | condition example                  | meaning                                                |
|------------------|---------------|:---------------------------:|------------------------------------|--------------------------------------------------------|
| url              | string        |             yes             | "url": ["github", "stackoverflow"] | url contains "github" _**or**_ "stackoverflow"         |
| id               | int           |             no              | -                                  | -                                                      |
| valid            | boolean       |             yes             | "valid": true                      | the url is valid(valid check haven't been implemented) |
| title            | string        |             yes             | (similar to `url`)                 | (similar to `url`)                                     |
| tags             | array         |             yes             | "tags": ["python", "javascript"]   | tags contains "python" _**or**_ "javascript"           |
| is_github_url    | boolean       |             yes             | (similar to `valid`)               | (similar to `valid`)                                   |
| github_repo_info | nested object |             no              | -                                  | -                                                      |
| time_added       | string        |             no              | -                                  | -                                                      |

All values in condition file is **case-sensitive**.

## Acknowledgments

- [tqdm](https://github.com/tqdm/tqdm)
- [revchatgpt](https://github.com/acheong08/ChatGPT)
- [ChatGPT](https://chat.openai.com/)
- [Diigo](https://www.diigo.com/)

## Contributing

We welcome you to join the development of tagmark. Please see [contributing document][contributing-document-url]

## TODO

- [x] lib.data: skip dumping some tagmark item according to user input
- [x] Tagmark.get_github_repo_infos add condition filter
- [x] add msg to show rate of process in `convert` command becuase it may be slow when there are a plenty of github repo urls
- [ ] lib.data: add github repo licence info into TagmarkItem
- [ ] validate url availability and set TagmarkItem.valid according to the result
  - [x] github repo url
  - [ ] not github repo url

[contributing-document-url]: https://github.com/pwnfan/tagmark/blob/main/.github/CONTRIBUTING.md
