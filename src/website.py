import logging
import os
import pathlib
import shutil

from blocks import markdown_to_html_node

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="copy-files-logs.log",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


def copy_files(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination, exist_ok=True)
    for content in os.listdir(source):
        source_path = os.path.join(source, content)
        destination_path = os.path.join(destination, content)
        if os.path.isfile(f"{source}/{content}"):
            shutil.copy(source_path, destination_path)
            logger.info(f"Copied {content} to {destination}")
        else:
            copy_files(source_path, destination_path)


def extract_title(markdown):
    if markdown.split("\n")[0].startswith("# "):
        return markdown.split("\n")[0][2:]
    raise Exception("No title found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        contents = f.read()
    with open(template_path, "r") as t:
        template = t.read()
    html_string = markdown_to_html_node(contents).to_html()
    title = extract_title(contents)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as t:
        t.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for content in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, content)
        destination_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(f"{dir_path_content}/{content}"):
            destination_path = str(pathlib.Path(destination_path)).replace(
                ".md", ".html"
            )
            generate_page(source_path, template_path, destination_path, basepath)
        else:
            generate_pages_recursive(
                source_path, template_path, destination_path, basepath
            )
