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

INPUT_DIR = "input/"

def load_files():
    for f in glob.glob(INPUT_DIR + '**/*.md', recursive=True):
        with open(f, 'r') as file:     
            generate_html(file)

def generate_html(file: typing.TextIO):
    global title_template, html_template, css_template
    page_title: str = title_template
    lines: list[str] = []

    # If the first line starts with $, we set that as the page title
    for i, line in enumerate(file):
        if i == 0 and line[0] == '$':
            page_title = line[1:].strip()
        else:
            lines.append(line)

    # Parse the markdown into HTML format
    # TODO: implement a markdown parser for more flexibility
    body: str = markdown.markdown('\n'.join(lines))

    contents: str = html_template
    contents = contents.replace("$TITLE", page_title)
    contents = contents.replace("$BODY", body)

    output_file_title: str = file.name.replace("input", "output").replace("md", "html")
    
    # Make the output file (and directories if they do not exist)
    output_file = Path(output_file_title)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(contents)

    print(f"Generated page: {file.name}")

def main():
    global config, title_template, html_template, css_template
    config.read("settings.ini")

    title_template = config['koishi']['title']
    html_template = config['koishi']['html']
    css_template = config['koishi']['css']

    # Load the .html and .css templates into memory
    try:
        with open(html_template, 'r') as file:
            html_template = ' '.join(file)

        with open(css_template, 'r') as file:
            css_template = ' '.join(file)

    except:
        sys.stderr.write("Template .html and/or .css files were not found! Check settings.ini to ensure the paths are valid and the files exist.")
        exit()

    load_files()
    print("Finished building website! Check output/ for the result.")

if __name__ == "__main__":
    main()
