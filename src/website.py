import logging
import os
import shutil

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
