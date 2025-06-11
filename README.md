# koishi
*koishi* is a simple and barebones static site generator.

> [!WARNING]
> This project is a WIP and generated results may not be as expected.

## Installation
*koishi* requires [Python-Markdown](https://pypi.org/project/Markdown/) to run.

```bash
pip install markdown
git clone https://github.com/epsilorne/koishi.git
cd koishi
```

## Usage

Markdown files are used to contain the content of webpages.
*koishi* will recursively search for `.md` files in the `input/` directory.
The default title for a page will be `DEFAULTTITLE`, but this can be changed by adding `$<CUSTOM TITLE>` to the first line of the markdown file.

To generate the site, run:
```bash
python build.py
```

The generated `.html` files will be located in the `output/` directory.

## Configuration
*koishi* can be customised in `conf.ini`:

```ini
[koishi]
# The default title of the page
title = DEFAULTTITLE

# Template .html and .css files
html=template/default.html
css=template/style.css

# Input .md and output .html directories
input_dir=input/
output_dir=output/
```

Furthermore, you can configure the template `.html` and `.css` files to your liking.
*koishi* injects the markdown contents, page title and stylesheet to wherever `$BODY`, `$TITLE` and `$CSS` are located, so you can use your own `.html` and have *koishi* insert the contents for you.
