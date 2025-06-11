import configparser
import glob
import markdown
from pathlib import Path
import typing
import sys

config = configparser.ConfigParser()

html_template: str
css_template: str
title_template: str
input_dir: str
output_dir: str

def generate_html(file: typing.TextIO):
    global title_template, html_template, css_template, input_dir, output_dir
    page_title: str = title_template
    lines: list[str] = []

    # If the first line starts with $, we set that as the page title
    for i, line in enumerate(file):
        if i == 0 and line[0] == '$' and len(line) > 1:
            page_title = line[1:].strip()
        else:
            lines.append(line)

    # Parse the markdown into HTML format
    # TODO: implement a markdown parser for more flexibility
    body: str = markdown.markdown('\n'.join(lines))

    contents: str = html_template
    contents = contents.replace("$TITLE", page_title)
    contents = contents.replace("$BODY", body)

    output_name: str = file.name.replace(input_dir, output_dir).replace("md", "html")

    # Make the output file (and directories if they do not exist)
    output_file = Path(output_name)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(contents)

    print(f"Generated page: {file.name}")

def main():
    global config, title_template, html_template, css_template, input_dir, output_dir

    # Parse the config file
    config.read("conf.ini")
    title_template = config['koishi']['title']
    html_template = config['koishi']['html']
    css_template = config['koishi']['css']
    input_dir = config['koishi']['input_dir']
    output_dir = config['koishi']['output_dir']

    # Load the .html and .css templates into memory
    try:
        with open(html_template, 'r') as file:
            html_template = ' '.join(file)

        with open(css_template, 'r') as file:
            css_template = ' '.join(file)

    except:
        sys.stderr.write("Template .html and/or .css files were not found! Check settings.ini to ensure the paths are valid and the files exist.")
        exit()

    # Recursively look for .md files to parse
    for f in glob.glob(input_dir+ '**/*.md', recursive=True):
        with open(f, 'r') as file:
            generate_html(file)

    print(f"Finished building website! Check {output_dir} for the result.")

if __name__ == "__main__":
    main()
