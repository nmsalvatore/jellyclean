import argparse
import os
from pathlib import Path
from time import sleep

from jellyclean.formatting import clean_file, clean_directory
from jellyclean.file_types import FileExtension
from jellyclean.log_config import logging


logger = logging.getLogger(__name__)


def process_directory(directory: Path) -> None:
    """Perform cleanup on contents of provided directory"""

    for entry in map(lambda e: (directory / e), os.listdir(directory)):
        if entry.name.endswith((FileExtension.MKV, FileExtension.MP4)):
            logger.info(f"Performing cleanup on {entry}")
            clean_file(directory, entry)

        if os.path.isdir(entry) and any(os.listdir(entry)):

            # check if directory contains movie or tv show
            #   if movie, clean_movie_directory
            #   if tv show, clean_tv_directory

            logger.info(f"Performing cleanup on {entry}")
            clean_directory(directory, entry)

        sleep(0.2)


def main() -> None:
    """Takes a CLI directory argument and cleans the provided directory"""

    parser = argparse.ArgumentParser(
        prog="JellyClean",
        description="A CLI tool for cleaning up a Jellyfin media directory",
    )
    parser.add_argument("directory", type=Path, help="Directory to clean")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        raise ValueError(f"{args.directory} is not a directory")

    process_directory(args.directory)


if __name__ == "__main__":
    main()
