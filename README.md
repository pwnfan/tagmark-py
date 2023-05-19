# tagmark (Python)

## What is TagMark

TagMark is a tag based browser bookmark solution for developers.

I have writien a blog [TagMark: Maybe a Better Browser Bookmark Solution](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/) to introduce TagMark in details with a toc below:

- [What is TagMark](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#what-is-tagmark)
- [What is a "browser bookmark solution"](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#what-is-a-browser-bookmark-solution)
- [Why we need tags for bookmarks](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#why-we-need-tags-for-bookmarks)
- [Why not Diigo bookmark manager (Diigo My Library)](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#why-not-diigo-bookmark-manager-diigo-my-library)
- [TagMark's solution: How to build your own TagMark](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#tagmarks-solution-how-to-build-your-own-tagmark)
- [Advanced usages](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#advanced-usages)

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
(testvenv) ➜ tagmark_cli convert --help
Usage: tagmark_cli convert [OPTIONS]

  covert other format of bookmarks into Tagmark format(json-lines)

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
                                  fitlering TagmarkItem  [default: /opt/homebr
                                  ew/Caskroom/mambaforge/base/envs/testvenv/li
                                  b/python3.11/site-
                                  packages/tagmark/condition_example.json]
  -b, --is-ban-condition BOOLEAN  If set to True, a TagmarkItem hits the
                                  `condition` will be banned, or it will be
                                  remained.  [default: True]
  -t, --github_token TEXT         the GITHUB_TOKEN to access Github API,
                                  default will read from the .env file of the
                                  root dir of this project
  --help                          Show this message and exit.
```

**Usage Examples**

```bash
# convert from Diigo output(Chrome format) into TagMark json-lines format file tagmark_ui_data.jsonl
(py311) ➜  tagmark_cli convert -i data/16400249_chrome_2023_04_24_0a65e.html -f diigo_chrome

# actually not for convertion, but for refreshing Github repo information in the file tagmark_ui_data.jsonl
# and output into a new file new_tagmark_ui_data.jsonl
(py311) ➜  tagmark_cli convert -i data/tagmark_ui_data.jsonl -f tagmark_jsonlines -o new_tagmark_ui_data.jsonl
```

## Core Options Explantation and Tagmark Details

-   `-f`: the input file [default: diigo_chrome]

    -   `diigo_chrome`: the Chrome format bookmarks exported from Diigo library, see [my blog](https://pwnfan.github.io/post/en/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/#tagmarks-solution) for details
    -   `tagmark_jsonlines`: indicate the input file is a tagmark format json-lines file, which is the output file of the `-o` option of this script. This may be confused, but it's not useless, the purpose of using a `-o` output file as the `-i` input file in a next run, is to refresh the Github info(Starts, Forks, Last Commit, etc) of the bookmarks who are Github repos.

-   `-k`: whether keep keys with empty values [default: False]. This is to opitmize the output file size by removing the keys with empty values.

-   `-c` and `-b`:

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

## Condition File Details

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

## Contributing

We welcome you to join the development of tagmark. Please see [contributing document][contributing-document-url]

## TODO

- [x] lib.data: skip dumping some tagmark item according to user input
- [ ] Tagmark.get_github_repo_infos add condition filter
- [ ] add msg to show rate of process in `convert` command becuase it may be slow when there are a plenty of github repo urls
- [ ] lib.data: add github repo licence info into TagmarkItem
- [ ] validate url availability and set TagmarkItem.valid according to the result

[contributing-document-url]: https://github.com/pwnfan/tagmark/blob/main/.github/CONTRIBUTING.md
