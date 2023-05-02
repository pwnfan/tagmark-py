# Tagmark

## Usage

```bash
(py311) ➜  tagmark git:(main) ✗ poetry run tagmark_cli --help                                      
Usage: tagmark_cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  convert  covert other format of bookmarks into Tagmark format(json-lines)
(py311) ➜  tagmark git:(main) ✗ poetry run tagmark_cli convert --help
Usage: tagmark_cli convert [OPTIONS]

  covert other format of bookmarks into Tagmark format(json-lines)

Options:
  -i, --input-file-path FILE      input file path
  -f, --format [diigo_chrome|tagmark_jsonlines]
                                  format of the input file  [default:
                                  diigo_chrome]
  -o, --output-file-path FILE     output file path  [default:
                                  ui/data/tagmark_ui_data.jsonl]
  -k, --keep_empty_keys BOOLEAN   whether keep keys with empty values
                                  [default: False]
  -t, --github_token TEXT         the GITHUB_TOKEN to access Github API,
                                  default will read from the .env file of the
                                  root dir of this project
  --help                          Show this message and exit.
```

examples:

```bash
(py311) ➜  poetry run tagmark_cli convert -i data/16400249_chrome_2023_04_24_0a65e.html -f diigo_chrome

(py311) ➜  poetry run tagmark_cli convert -i data/tagmark_ui_data.jsonl -f tagmark_jsonlines
```

## Development

## Test

in the root directory of this project

```bash
# create a file `.env` containing github aceess token
echo "GITHUB_TOKEN=github_pat_XXX" > .env

# run test
poetry run pytest -v --cov=tagmark tests/
```

## Contributing

We welcome you to join the development of TagMark. Please see [contributing document][contributing-document-url]

## TODO

* [ ] lib.data: skip dumping some tagmark item according to user input
* [ ] lib.data: add github repo licence info into TagmarkItem

[contributing-document-url]: https://github.com/pwnfan/tagmark/blob/main/.github/CONTRIBUTING.md
