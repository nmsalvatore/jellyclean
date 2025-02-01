import argparse
import logging
import os
from pathlib import Path

from jellyclean.formatting import clean_file, clean_directory
from jellyclean.file_types import FileExtension


logging.basicConfig(format="%(message)s", level=logging.DEBUG)


def process_directory(directory: Path) -> None:
    """Perform cleanup on contents of provided directory"""

    for entry in map(lambda e: (directory / e), os.listdir(directory)):
        if entry.name.endswith((FileExtension.MKV, FileExtension.MP4)):
            clean_file(directory, entry)

        if os.path.isdir(entry):
            clean_directory(directory, entry)

        else:
            continue


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
