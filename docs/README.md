# tagmark (Python)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tagmark)
[![codecov](https://codecov.io/gh/pwnfan/tagmark-py/branch/main/graph/badge.svg?token=KKNE7A09N5)](https://codecov.io/gh/pwnfan/tagmark-py)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/80e261999e2445f4b825e646cb41b1a5)](https://app.codacy.com/gh/pwnfan/tagmark-py/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Release & Upload To PyPI](https://github.com/pwnfan/tagmark-py/actions/workflows/release.yml/badge.svg)](https://github.com/pwnfan/tagmark-py/actions/workflows/release.yml)
[![Test](https://github.com/pwnfan/tagmark-py/actions/workflows/test.yml/badge.svg)](https://github.com/pwnfan/tagmark-py/actions/workflows/test.yml)
[![Twitter Follow](https://img.shields.io/twitter/follow/pwnfan?label=follow)](https://twitter.com/intent/follow?screen_name=pwnfan)
[![Twitter URL](https://img.shields.io/twitter/url?url=https%3A%2F%2Ftwitter.com%2Fintent%2Ftweet%3Ftext%3Dhttps%3A%2F%2Fgithub.com%2Fpwnfan%2Ftagmark-py)](https://twitter.com/intent/tweet?text=https://github.com/pwnfan/tagmark-py) 


- [1. Introduction, User Guide and the Demo Page](#1-introduction-user-guide-and-the-demo-page)
- [2. Why TagMark?](#2-why-tagmark)
- [3. TagMark Related Projects](#3-tagmark-related-projects)
- [4. TagMark Architecture, Workflow and Customizing Guide](#4-tagmark-architecture-workflow-and-customizing-guide)
- [5. tagmark-py User Guide](#5-tagmark-py-user-guide)
  - [5.1. Installation](#51-installation)
  - [5.2. Usage](#52-usage)
    - [5.2.1. subcommand: export](#521-subcommand-export)
    - [5.2.2. subcommand: convert](#522-subcommand-convert)
    - [5.2.3. subcommand: checktag](#523-subcommand-checktag)
    - [5.2.4. subcommand: autotagdef](#524-subcommand-autotagdef)
    - [5.2.5. subcommand: maketagdoc](#525-subcommand-maketagdoc)
    - [5.2.6. Condition File Details](#526-condition-file-details)
  - [5.3. Changelog](#53-changelog)
  - [5.4. Contributing and Development Guide](#54-contributing-and-development-guide)
  - [5.5. TODO](#55-todo)
  - [5.6. Credits](#56-credits)
- [6. Similar Tools / Projects](#6-similar-tools--projects)

## 1. Introduction, User Guide and the Demo Page

TagMark is a tag-based bookmark solution I created for:

* Those who have a multitude of bookmarks and want to efficiently organize, easily retrieve, and share them with others.
* Individuals who frequently work with GitHub, have starred numerous repositories, yet struggle with how to efficiently retrieve and effectively utilize this vast amount of information.

Watch this video `TagMark - Introduction and User Guide` for details: 

[![TagMark - Introduction and User Guide](https://img.youtube.com/vi/0F5bkU90Tmc/0.jpg)](https://youtu.be/0F5bkU90Tmc)

Here is the demo page of TagMark, which collected all my bookmarks:

<https://pwnfan.github.io/my-tagmarks> / <https://tagmark.pwn.fan>

Features of the page:

- Substantial tag based bookmarks
  - 2700+ tagged bookmarks (1800+ curated Github Repos) mainly focus on cybersecurity and related development
  - 1000+ tags with detailed tag definitions
- Full featured tags
  - tag definitions (show / hide definition by left click on tags)
  - tag overview with counts
  - color difference depending on counts
- Simple but powerful header filter for each column
  - thick client: static, pure frontend and js based, so it's fast responding
  - simple and useful filter grammar
  - quickly input tag name into filter by just a right click
  - press CTRL/CMD with left click in any filter input to call out multiple language document (English / Japanese / Chinese)
- Supporting for URL GET parameters based filtering
  - static, pure frontend and js based
  - easy for sharing
- Columns related things
  - detailed Github repository information
  - suppressible columns
- Template Tag Doc

## 2. Why TagMark?

The introduction video summarized the reasons why I made TagMark, for the detailed reasons you can read my blog (`TL;DR 😅`)  [TagMark: Maybe a Better Browser Bookmark Solution](https://pwnfan.github.io/en/post/TagMark-Maybe-a-Better-Browser-Bookmark-Solution/)

## 3. TagMark Related Projects

* [tagmark-py (this repo)](https://github.com/pwnfan/tagmark-py)
  * exporting tagged bookmarked data from other third party services, e.g. diigo
  * converting other bookmark formats into Tagmark format, i.e `tagmarks.jsonl`
  * checking every tag has a been defined, i.e. checking tag consistency in `tagmarks.jsonl` and `tags.json`
  * getting tag definitions automatically with ChatGPT, i.e setting the values of the key `definition` in `tags.json`
  * making document from a template containing tag related syntaxes, i.e making `tag-doc.md`
* [tagmark-ui](https://github.com/pwnfan/tagmark-ui)
  * a web page showing `tagmarks.jsonl`, `tags.json` and related docs
* [my-tagmarks](https://github.com/pwnfan/my-tagmarks)
  * my own bookmarks data stored as TagMark data `tagmarks.jsonl` and `tags.json`
  * a Github Pages repo serving `tagmark-ui` and showing all my bookmarks, i.e <https://pwnfan.github.io/my-tagmarks> / <https://tagmark.pwn.fan>
  * a Github README including curated topics (i.e. tags) from my personal bookmarks

## 4. TagMark Architecture, Workflow and Customizing Guide

If you want to customize your own `my-tagmarks`, here is a overview of TagMark architecture and workflow you need to get familiar with:

```text
     │                                                                         https://pwnfan.github.io/my-tagmarks    
   #0│   ╔═════════════╗          ╔═══════════════╗       ╔═════════════════╗  i.e. https://tagmark.pwn.fan            
   start ║  [original  ║          ║[exported data]║       ║  {tagmark-py}   ║                     ▲                    
     └──>║  bookmark   ║          ║               ║       ║   (this repo)   ║            #9 deploy│Github Pages        
         ║    data]    ║          ║ ░diigo░tool░░ ║       ║                 ║                     │                    
         ║             ║    ┌─────║>exported░data ║       ║   ████████████  ║  ┌──────────────────┼────────┐           
         ║ ░pwnfan's░░ ║    │     ║ ░░░(.html)░░░ ║ ┌──#2b.2──█subcommand█  ║  │         ╔════════════════╗│           
    ┌────║─░untagged░░ ║    │     ║               ║ │     ║   ███export███  ║  │         ║ {my-tagmarks}  ║│  #6.1     
    #1   ║ ░bookmarks░ ║    │     ║ ░░diigo░API░░ ║─┼──┐  ║   ████████████<─║──┼─┐       ║   ┌────────┐  ┌║┼──manually─
 manually║             ║    │     ║ ░dumped░data░<║─┘ #3.1║any              ║  │ │       ║   │tag-doc.│  │║│  make     
 set│tags╚═════════════╝    │     ║ ░░(.jsonl)░░░ ║   format  ████████████<─║──┘ │ ┌─#6.2║───│template│<─┘║│           
 and│add                  #2a.2   ╚═══════════════╝    └──║──>█subcommand█  ║    │ │     ║   └────────┘   ║│ #7.1      
   into                     │                             ║   ██convert███──║─┐  │ │     ║  ┌──────────┐  ║│update     
    │ ╔══════════════════╗  │    #3.2 add Github┌repo─────║───████████████  ║ │  │ │   ┌─║─>│tag-doc.md│  ║│Github     
    │ ║   {third-party   ║  │    info and covert│into     ║                 #7.2 │ │ #6.3║  └──────────┘  ║│ repo      
    │ ║bookmark & tagging║  │                   │         ║   ████████████  ║ │  │ │   │ ║   ┌────────┐   ║│ info      
    │ ║     service}     ║  │    ╔═════════════╗│ ┌──#4.1─║──>█subcommand█  ║ └──┼─┼───┼─║──>│tagmarks├───║everyday    
    │ ║                  ║  │    ║  [TagMark   ║│ │       ║   ██checktag██  ║    │ │ ┌─┼─║──>│ .json  │   ║            
    │ ║    ███diigo███   ║  │    ║    data]    ║│ │  ┌────║───████████████  ║    │ │ │ │ ║   └────────┘   ║            
    └─║───>██browser██   ║  │    ║             ║│ │ #4.2 add                ║    │ │ │ │ ║  ┌─────────┐   ║            
      ║    █extension█   ║  │  ┌─║──░░░░░░░░░<─║┘ │ missing   ████████████  ║    │ │┌┼─┼─║─>│tags.json│   ║            
      ║         │        ║  │ #3.3  ░TagMark░  ║  │ tags  ║   █subcommand█  ║    │ │││ │ ║  └─────────┘   ║            
      ║         │        ║  │  │ ║  bookmarks  ║  │  │    ║   █autotagdef█  ║    │ │││ │ ║  ┌──────────┐  ║            
      ║         ▼        ║  │  │ ║  (tagmarks  ║──┘  │ ┌#5.1─>████████████──║──┐ │ │││ │ ║  │tagmark-ui│  ║            
      ║    ███diigo███   ║  │  │ ║  ░.jsonl)░  ║     │ │  ║                 ║  │ │ │││ │ ║  └────▲─────┘  ║            
      ║    ██website██   ║  │  │ ║  ░░░░░░░░░  ║     │ │  ║   ████████████  ║  │ │ │││ │ ║       │        ║            
      ║         │        ║  │  │ ║             ║─────┼─┼#6.1─>█subcommand█<─║──┼─┼─┘││ │ ╚══════#8════════╝            
      ║         │  #2a.1 ║  │  │ ║ ░░░░░░░░░░░ ║     │ │  ║   █maketagdoc█──║──┼─┼──┼┼─┘         │                     
      ║         │ manually  │  │ ║ ░░TagMark░░<║─────┘ │  ║   ████████████  ║  │ │  ││  ╔═══════════════════╗          
      ║ ┌───────┴──run─on║  │┌─┼─║>░tags░info░─║───────┘  ╚═════════════════╝  │ │  ││  ║   {tagmark-ui}    ║          
      ║ │        diggo page ││ │ ║ (tags.json)<║─#5.2─define─tags─with─ChatGPT─┘ │  ││  ║ ┌──────────┐      ║          
      ║ │              │ ║  ││ │ ║ ░░░░░░░░░░░─║──────────#5.3───────────────────┼──┘│  ║ │filter doc├─┐    ║          
      ║ ▼              ▼ ║  ││ │ ║      │      ║                                 │   │  ║ │(EN/CN/JP)│ ├──┐ ║          
      ║ █diigo█ █diigo██ ║  ││ │ ╚═════════════╝                                 │   │  ║ └─┬────────┘ │  │ ║          
      ║ web█API █export█─║──┘│ │        │                                        │   │  ║   └──┬───────┘  │ ║          
      ║ ███████ ██tool██ ║   └─┼─────#4.3 manually set the values of keys        │   │  ║      └──────────┘ ║          
      ║   │              ║     │     `abbr/alias/full_name/gpt_prompt_context    │   │  ║  ┌─────────────┐  ║          
      ╚══════════════════╝     │     /prefer_format` for new added tags          │   │  ║  │Web Page Code│  ║          
          │                    │                                                 │   │  ║  └─────────────┘  ║          
          │                    └─────────────────────────────────────────────────┼───┘  ╚═══════════════════╝          
          └────────────────────────────#2b.1─respond─to──────────────────────────┘                                     
                                                                                                                       
                                                                                                                       
Steps Flow:                                                                                                            
              (option a)     ┌─>#3.1────>#3.2────>#3.3  ┌──>#5.1────>#5.2────>#5.3──┐  ┌─────────────┐                 
          ┌─>#2a.1──>#2a.2───┤                     │    │                       │   └─>│ #7.1───>7.2 │                 
      #1──┤                  │    ┌────────────────┘    │     ┌─────────────────┘      │             │                 
          └─>#2b.1──>#2b.2───┘    ▼                     │     ▼                     ┌─>│   #8   #9   │                 
              (option b)        #4.1────>#4.2────>#4.3──┘   #6.1────>#6.2────>#6.3──┘  └─────────────┘                 
                                               (suggested)  (------optional-------)                                     
```

Steps note and customizing suggestions:

* Steps requiring manual works
  * #1:
    * the first time involves a full workload of tagging all your bookmarks, which may take a considerable amount of time, but subsequent efforts only involve incremental tasks, which are much more easier
    * diigo related resources
      * [Chrome Extension: Diigo Web Collector - Capture and Annotate](https://chrome.google.com/webstore/detail/diigo-web-collector-captu/pnhplgjpclknigjpccbcnmicgcieojbh)
      * [Diigo Website](https://www.diigo.com/)
      * [Diigo Tools / Export](https://www.diigo.com/tools/export)
  * #2a.x
    * use alternative #2b is suggested
    * #2a.1 does't work well recently, may be due to some problems on the [Diigo Tools / Export](https://www.diigo.com/tools/export) service side，which impelled me to made an alternative #2b instead
    * notice that #2b exploits a web API of diigo and acts like a crawler to retrieve your own bookmarks, it's a trade-off option so we'd better not frequently use it, and I have added some sleep time between successive requests
    * Diigo has [its own official API](https://www.diigo.com/api_keys/new/) for retrieving bookmarks but it is a premium (paid) feature, may be it's a better option to become a premium user and add the related retrieving feature (plugin) into `tagmark-py` `export` subcommand
  * #4.3
    * optional but suggested if you want reading-friendly tag names and exact tag definitions shown in the web page (i.e. tagmark-ui)
    * similar to #1, the first time involves a full workload, which may take a considerable amount of time, but subsequent efforts only involve incremental tasks and are much more easier
  * #6.x
    * optional, if you don't need a TagMark tag doc, you can skip these steps
    * may take a considerable amount of time if you have many bookmarks and tags, and want to well categorize them into different topics, but fortunately this is just an one-off work
* #7, #8, and #9 form a unit in which the prerequisite dependencies are Steps #1 through #6. However, Steps #7, #8, and #9 are independent of each other and have no interdependencies
* Some steps are auto done by Github Actions, most of which are located in repo `my-tagmarks`
  * to ensure these actions function correctly, you may need to set repo `vars` and `secrets` which will be used in these actions
    * #6.2 and #6.3
      * [my-tagmarks/.github/workflows/update-tag-doc.yml](https://github.com/pwnfan/my-tagmarks/blob/main/.github/workflows/update-tag-doc.yml)
        * `${{ secrets.GH_PAT_TAGMARK }}`
    * #7:
      * [my-tagmarks/.github/workflows/update-tagmark-data.yml](https://github.com/pwnfan/my-tagmarks/blob/main/.github/workflows/update-tagmark-data.yml)
        * `${{ secrets.GH_PAT_TAGMARK }}`
        * `${{ vars.TAGMARK_DATA_EXPIRED_HOURS }}`
    * #8: trigger when `tagmark-ui` has new commit
      * [tagmark-ui/.github/workflows/github-page-update.yml](https://github.com/pwnfan/tagmark-ui/blob/main/.github/workflows/github-page-update.yml): used to notify repo `my-tagmarks` of the `tagmark-ui` code updates, if you do not need this feature, you can disable it and skip setting repo `vars` and `secrets`
        * `${{ secrets.GH_PAT_TAGMARK }}`
        * `${{ vars.GH_PAGES_REPO }}`
      * [my-tagmarks/.github/workflows/update-tagmark-ui.yml](https://github.com/pwnfan/my-tagmarks/blob/main/.github/workflows/update-tagmark-ui.yml): used to receive the notify from `tagmark-ui` and synchronize the `tagmark-ui` code into `my-tagmarks`, if you do not need this feature, you can disable it and skip setting repo `vars` and `secrets`
        * `${{ secrets.GH_PAT_TAGMARK }}`
        * `${{ env.TAGMARK_UI_DIR }}`
    * #9
      * [my-tagmarks/.github/workflows/github_pages.yml](https://github.com/pwnfan/my-tagmarks/blob/main/.github/workflows/github_pages.yml): no `vars` and `secrets` needed
  * so the repo `vars` and `secrets` need to set are
    * `${{ secrets.GH_PAT_TAGMARK }}`
      * it is a personal access tokens (aka PAT) having the `Contents(Read and Write access to code)` permission to the code of repo `my-tagmarks`
      * you need to set it in both `tagmark-ui` and `my-tagmarks` if you need the UI code synchronizing feature 
    * `${{ vars.TAGMARK_DATA_EXPIRED_HOURS }}`
      * it determines the expiring time of the Github repo info to a bookmark, see `tagmark-py` subcommand `covert` for details
      * the value I've set is `23`
      * only need to be set in repo `my-tagmarks`

## 5. tagmark-py User Guide

### 5.1. Installation

1. install Python >=3.11 and a virtual environment (virtualenv / pyenv / conda)
2. install `tagmark-py`
    ```bash
    pip install tagmark
    ```
3. check tagmark runs well
    command line options:
    ```bash
    (tagmark-py3.11) vscode ➜ /workspaces/tagmark-py (dev) $ tagmark_cli 
    Usage: tagmark_cli [OPTIONS] COMMAND [ARGS]...

    Options:
      -h, --help  Show this message and exit.

    Commands:
      export      export tagged bookmarked data from third party services...
      convert     convert other bookmark formats into TagMark format...
      checktag    check tag consistency in tagmark data file (json-lines) and...
      autotagdef  get tag definition automatically with ChatGPT
      maketagdoc  make document from a template containing tag related syntaxes
    ```

### 5.2. Usage

#### 5.2.1. subcommand: export

```bash
(tagmark-py3.11) vscode ➜ /workspaces/tagmark-py (dev) $ tagmark_cli export -h
Usage: tagmark_cli export [OPTIONS]

  export tagged bookmarked data from third party services into jsonlines file

Options:
  -f, --format [diigo_web]        third party service  [default: diigo_web]
  -m, --max-sleep-seconds-between-requests FLOAT
                                  if multiple requests are needed to retrieve
                                  the data, in order to prevent excessive load
                                  on the target server, a random time sleep is
                                  necessary, this option set the maximum sleep
                                  seconds  [default: 3]
  -o, --output-file-path FILE     output file path  [default:
                                  diigo_web_exported.jsonl]
  -h, --help                      Show this message and exit.
```

* `export` retrieves bookmarks data (with tags) from third party bookmark manager services which support tags
* even though `-f diigo_web` is the only supported third party service now, `export` subcommand is designed to supported different services
* `-f diigo_web` requires the diigo web cookie and reads its value from the key `DIIGO_COOKIE` stored in the .env file or environment variables, so you need to set it before run `export`
  .env file example:
  ```bash
  DIIGO_COOKIE="{YOUR DIIGO WEB COOKIE HERE}"
  ```
* setting `-m, --max-sleep-seconds-between-requests` to more than `3` is recommended, though it may take longer to retrieve the whole data
* note that `export` is different from other subcommands, if you run `tagmark_cli export` without any arguments, it will not print the help message, instead it will run directly with the default values of the arguments

#### 5.2.2. subcommand: convert

```bash
(tagmark-py3.11) vscode ➜ /workspaces/tagmark-py (dev) $ tagmark_cli convert 
Usage: tagmark_cli convert [OPTIONS]

  convert other bookmark formats into TagMark format (json-lines)

Options:
  -i, --input-file-path FILE      input file path
  -f, --format [diigo_web_exported|diigo_exported_chrome_format|tagmark_jsonlines]
                                  format of the input file  [default:
                                  diigo_web_exported]
  -o, --output-file-path FILE     output tagmark jsonlines data file path
                                  [default: tagmarks.jsonl]
  -k, --keep_empty_keys BOOLEAN   whether keep keys with empty values
                                  [default: False]
  -c, --condition-json-path FILE  json file containing the condition for
                                  fitlering TagmarkItem  [default:
                                  /workspaces/tagmark-
                                  py/tagmark/condition_example.json]
  -b, --is-ban-condition BOOLEAN  If set to True, a TagmarkItem hits the
                                  `condition` will be banned, or it will be
                                  remained  [default: True]
  -t, --github_token TEXT         the GITHUB_TOKEN to access Github API,
                                  default will read from the .env file of the
                                  root dir of this project
  -u, --update-github-info-after-hours FLOAT
                                  update github info only when user specified
                                  number of hours has passed since the last
                                  update  [default: 23]
  -h, --help                      Show this message and exit.
```
* `convert` helps to convert other bookmark formats (i.e. `-f diigo_web_exported | diigo_exported_chrome_format`) into TagMark data file (json-lines) and add Github info for Github repo bookmarks
  command example:
  ```bash
  tagmark_cli convert -i tagmarks_all.jsonl -f diigo_web_exported -c data/my-condition.json
  ```
* `convert` can also be used to only update the Github repo info (stars, late commit data, etc) of a converted TagMark data file (json-lines) (i.e. `-f tagmark_jsonlines`)
  command example:
  ```bash
  tagmark_cli convert -i data/tagmark_ui_data.jsonl -c data/my-condition.json -f tagmark_jsonlines
  ```
* before running `covert`, you may need setup Github PAT, if you don't have any Github Repo Bookmarks, this step can be skipped
  * [create a github personal access token(PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
  * `tagmark` requires PAT to access the Github API to get the repo info(stars, forks etc.) when a bookmark url is a Github repo url. The default settings to the PAT is recommended, which has no any privilege for any action to any of your repos or settings.
  * `export` reads the Github PAT from key `GITHUB_TOKEN` stored in the .env file or environment variables
    .env file example:
    ```bash
    GITHUB_TOKEN=github_pat_XXX
    ```
  * you can also tell `export` your Github PAT by adding the `-t` parameter, which is no recommended because it may remain in your bash history
* if you have bad network connection to Github API server (access from China, e.g.), you may got a lot connection errors when `convert` tries to get Github repo info, in this case you may need to continue to run `convert -f tagmark_jsonlines` again and again until all the missed Github repo info have been completed
* please refer to section [Core Options Explanation and Design Details](#core-options-explantation-and-design-details) for details of the options.

#### 5.2.3. subcommand: checktag

```bash
(tagmark-py3.11) vscode ➜ /workspaces/tagmark-py (dev) $ tagmark_cli checktag
Usage: tagmark_cli checktag [OPTIONS]

  check tag consistency in tagmark data file (json-lines) and tags info file
  (json)

Options:
  -d, --tagmark-jsonlines-data-path FILE
                                  the tagmark jsonlines data file path, which
                                  may be the output file generated by the `-o`
                                  parameter of the `convert` subcommand
  -t, --tags-json-path FILE       tags.json file path
  -c, --condition-json-path FILE  json file containing the condition for
                                  filtering TagmarkItem, here only the value
                                  of `tags` field in the file will be used,
                                  and this condition must be a ban condition
                                  [default: /workspaces/tagmark-
                                  py/tagmark/condition_example.json]
  -a, --add-new-tags BOOLEAN      if set to `True`, a new tags.json file will
                                  be generated, which includes old tags in
                                  tag.json file, and new tags in the tagmark
                                  data file(specified by -t).  [default: True]
  -h, --help                      Show this message and exit.
```


* `checktag` helps to verify if every tag in the output file generated by the `-o` parameter of the `convert` subcommand has relate tag info in the tag info json file. This ensures the web UI [tagmark-ui](https://github.com/pwnfan/tagmark-ui) functions correctly.
  command example:
  ```bash
  tagmark_cli checktag -d data/tagmarks.jsonl -t data/tags.json -c data/my-condition.json
  ```
* if you specify `-a true` to run `checktag`, tags only in tagmark json lines data but not in tags info json file will be added and output to a new tags info json file, before jump into the next step, you may need to manually check the newly added tags in the new tags json file
  * you can find them by searching `"definition": null`
  * in most cases you need to manually set the values of keys `abbr/alias/full_name/gpt_prompt_context` for the new tags, which is the step #4.3 in the TagMark workflow diagram
  * this step is strongly suggested if you want reading-friendly tag names and exact tag definitions shown in the web page (i.e. tagmark-ui) 
* if you run `checktag` for the first time, i.e. you don't hava a tags info json file (tags.json), you need to make an empty one by run:
  ```bash
  echo "{}" > tags.json
  ```

#### 5.2.4. subcommand: autotagdef

```bash
(tagmark-py3.11) vscode ➜ /workspaces/tagmark-py (dev) $ tagmark_cli autotagdef
Usage: tagmark_cli autotagdef [OPTIONS]

  get tag definition automatically with ChatGPT

Options:
  -d, --tags-info-json-path FILE  tags.json (tags information) file path
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
  -t, --gpt-timeout INTEGER       the timeout that GPT answers one question
                                  (get one tag definition)  [default: 60]
  -l, --little-info-tag-is-ok BOOLEAN
                                  [default: False]
  -h, --help                      Show this message and exit.
```

* `autotagdef` helps to get tag definition automatically from ChatGPT
  command example:
  ```bash
  tagmark_cli autotagdef -d data/tags.json -c gpt_config.json -l true
  ```
* how it work?
  for example a user edited tag info (Step #4.3 in TagMark workflow diagram):
  ```json
  "bom": {
      "abbr": "BOM",
      "alias": null,
      "definition": null,
      "full_name": "Bill of Materials",
      "gpt_prompt_context": "computer science and cybersecurity",
      "prefer_format": "{abbr} ({full_name})"
  }
  ```
  `autotagdef` will ask ChatGPT with prompt "in {gpt_prompt_context}, what is {prefer_format}?", i.e. "in computer science and cybersecurity, what is BOM (Bill of Materials)?", and set the value of key `"definition"` according to the response from ChatGPT
* the `-l, --little-info-tag-is-ok` option is applying for tags like:
  ```json
  "checklist": {
      "abbr": null,
      "alias": null,
      "definition": null,
      "full_name": null,
      "gpt_prompt_context": null,
      "prefer_format": "{tag}"
  }
  ```
  if `-l true` is set, then question will be sent to ChatGPT, i.e "what is checklist?"
  or if `-l false` is set (default value), an error `NoEnoughTagInfoForGptPromptException` will be raised
  this option is for ensuring that user didn't miss editing any tag info
* just like the `convert` subcommand, if you have bad network connection (access from China, e.g.) to OpenAI API server (Or maybe a API proxy server for the revChatGPT lib) , you may got a lot connection errors when `autotagdef` tries to ask ChatGPT, in this case you may need to continue to run `autotagdef -f tagmark_jsonlines` again and again until all the tags have got a definition from ChatGPT
* `autotagdef` use the python lib [revChatGPT](https://github.com/acheong08/ChatGPT) to communicate with ChatGPT
  * but unfortunately [revChatGPT](https://github.com/acheong08/ChatGPT) was archived in 2023.08.10, I am not sure how long it will remain functional
  * maybe I need to find an alternative lib for [revChatGPT](https://github.com/acheong08/ChatGPT), if you got related errors in running `autotagdef`, please tell me in the issue of this repo
* `-c, --gpt-config-file-path` is required for [revChatGPT](https://github.com/acheong08/ChatGPT), and a config file content looks like:
  ```json
  {
  "access_token": "{YOUR_ACCESS_TOKEN}"
  }
  ```
  and `access_token` can be got by accessing <https://chat.openai.com/api/auth/session>

#### 5.2.5. subcommand: maketagdoc

```bash
(tagmark-py3.11) vscode ➜ /workspaces/tagmark-py (dev) $ tagmark_cli maketagdoc
Usage: tagmark_cli maketagdoc [OPTIONS]

  make document from a template containing tag related syntaxes

Options:
  -d, --tagmark-jsonlines-data-path FILE
                                  the tagmark jsonlines data file path, which
                                  may be the output file generated by the `-o`
                                  parameter of the `convert` subcommand
  -t, --tags-json-path FILE       tags.json file path
  -s, --config-path FILE          (formatter) configuration file path
                                  [default: /workspaces/tagmark-
                                  py/tagmark/tools/maketagdoc.toml.default]
  -u, --url-base TEXT             url base for generating formatted links
                                  [default: ./]
  -c, --condition-json-path FILE  json file containing the condition for
                                  filtering TagmarkItem, here only the value
                                  of `tags` field in the file will be used,
                                  and this condition must be a ban condition
                                  [default: /workspaces/tagmark-
                                  py/tagmark/condition_example.json]
  -b, --is-ban-condition BOOLEAN  If set to True, a TagmarkItem hits the
                                  `condition` will be banned, or it will be
                                  remained  [default: True]
  -m, --template-path FILE        template file path
  -o, --output-file-path FILE     the output file (formatted according to the
                                  template file) path  [default:
                                  /workspaces/tagmark-py/formatted_tag_doc.md]
  -h, --help                      Show this message and exit
```

* `maketagdoc` make document from a template containing tag related syntaxes, a config file is also required but there is a default value for it
  command example:
  ```bash
  tagmark_cli maketagdoc -d data/tagmarks.jsonl -u https://pwnfan.github.io/my-tagmarks/ -t data/tags.json -m data/maketagdoc/tag-doc.template -o data/maketagdoc/tag-doc.md
  ```
* though I use `maketagdoc` to make markdown format tag doc in `my-tagmarks`, actually `maketagdoc` can be generated as any doc format
  * if you want make other format tag doc (HTML, e.g.), you may need to customize your own config file and pass it to `-s, --config-path` parameter
  * making other format tag doc may need to read and debug the source code
    * [tagmark-py/tagmark/tools/maketagdoc.py](https://github.com/pwnfan/tagmark-py/blob/main/tagmark/tools/maketagdoc.py)
    * [tagmark-py/tagmark/tools/maketagdoc.toml.default](https://github.com/pwnfan/tagmark-py/blob/main/tagmark/tools/maketagdoc.toml.default)
    * [tagmark-py/tests/tools/test_maketagdoc.py](https://github.com/pwnfan/tagmark-py/blob/main/tests/tools/test_maketagdoc.py)
* if you just want to make your own markdown doc `tag-doc.md`, just refer to these template files about how to apply TagMark tag doc template syntaxes:
  * [tagmark-py/tests/data/maketagdoc_template.md](https://github.com/pwnfan/tagmark-py/blob/main/tests/data/maketagdoc_template.md)
  * [my-tagmarks/docs/tag-doc.template](https://github.com/pwnfan/my-tagmarks/blob/main/docs/tag-doc.template)

#### 5.2.6. Condition File Details

you may have noticed that some subcommand have these parameters:

* `-c, --condition-json-path FILE`
* `-b, --is-ban-condition BOOLEAN`

condition file was not included in the architecture and workflow diagram to avoid becoming too complicated to understand.

Here we will talk about the workflow containing condition file:

```bash
                                            ┌──────────────┐
                                            │      -b      │
                                            │  This is a   │
                                            │ban-condition?│
                    ┌────────────┐          └───────┬──────┘
                    │TagmarkItem │                  │
                    │┌───────────┴┐                 ▼
┌───────────┐       └┤TagmarkItem │        ┌────────────────┐       ┌──────────┐
│  TagMark  │        │┌───────────┴┐──────>│Filter Condition│──────>│Subcommand│
│ Data File │───────>└┤TagmarkItem │       └────────────────┘       │Processing│
└───────────┘         │ ┌──────────┴─┐              ▲               └──────────┘
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

you can treat this json structure as the data structure of a TagmarkItem, `-c` condition file and `-b` specify a filter telling tagmark if or not to output a TagmarkItem into the `-o` output file.

for example, if you _**do not**_ need any lines with tag `javascript` _**or**_ `css` to be output in the output file, you should specify your condition file by `-c my_condition.json` with the content below:

```json
{
    "tags": ["javascript", "css"],
}
```

and you need to specify the `-b True (default)` option, which means if a TagmarkItem meets the condition, it will be banned and will not be exported into to output file.

On the contrary, if you only need lines with tag `javascript` _**or**_ `css` to be output into the output file, you need to specify the `-b False` option, which means if a TagmarkItem meets the condition, it will be picked out(not banned) and put into the output file.

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

### 5.3. Changelog

see [docs/CHANGELOG.md](CHANGELOG.md)

### 5.4. Contributing and Development Guide

Welcome you to join the development of tagmark. Please see [docs/CONTRIBUTING.md](CONTRIBUTING.md)

### 5.5. TODO

- [x] lib.data: skip dumping some tagmark item according to user input
- [x] Tagmark.get_github_repo_infos add condition filter
- [x] add msg to show rate of process in `convert` command because it may be slow when there are a plenty of github repo urls
- [ ] lib.data: add github repo license info into TagmarkItem
- [ ] validate url availability and set TagmarkItem.valid according to the result
  - [x] github repo url
  - [ ] not github repo url
- [ ] automatically find a forked repo of invalid github repo, replace the old repo url with forked repo url, and add comment to explain why
- [x] update github info only when user specified number of hours has passed since the last update.
- [x] add subcommand ~~`cheatsheet`~~ `maketagdoc` to make a cheat sheet from a pre-defined template file
- [ ] add test case for `cli.py`
- [ ] make customized tag supporting bookmark collector for TagMark

### 5.6. Credits

* [Diigo](https://www.diigo.com/)
* [ChatGPT](https://chat.openai.com/)

## 6. Similar Tools / Projects

* tag supporting bookmark manager (`tagmark-py` & `tagmark-ui` alternative)
  * [Diigo](https://www.diigo.com/): Better reading and research with annotation, highlighter, sticky notes, archiving, bookmarking & more.
* cybersecurity tool collection with tags (`my-tagmarks` alternative)
  * [offsec.tools](https://offsec.tools/): A vast collection of security tools for bug bounty, pentest and red teaming
  * [WebHackersWeapons](https://github.com/hahwul/WebHackersWeapons): Web Hacker's Weapons / A collection of cool tools used by Web hackers.
