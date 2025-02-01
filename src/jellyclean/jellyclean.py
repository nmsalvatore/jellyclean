import argparse
import logging
import os
from pathlib import Path
from shutil import rmtree

from jellyclean.file_types import FileExtension
from jellyclean.formatting import reformat
from jellyclean.subtitles import (
    extract_clean_subtitles,
    is_subtitle_directory,
)


logging.basicConfig(format="%(message)s", level=logging.DEBUG)


def clean_dir(directory: Path) -> None:
    """Perform cleanup on contents of provided directory"""

    for entry in map(lambda e: Path(directory, e), os.listdir(directory)):
        subtitle_count: int = 1

        if not os.path.isdir(entry):
            # TODO: if just a movie file, reformat and create parent directory
            continue

        logging.info(f"Performing cleanup on {entry}")

        clean_dirname: str = reformat(entry.name)

        for subentry in map(lambda e: Path(entry, e), os.listdir(entry)):
            if subentry.name.endswith((FileExtension.MKV, FileExtension.MP4)):
                clean_filename: str = reformat(subentry.name)
                os.rename(subentry, (entry / clean_filename))

            elif subentry.name.endswith(FileExtension.SRT):
                os.rename(
                    (entry / subentry),
                    (entry / f"{clean_dirname}.eng.{subtitle_count}.srt")
                )
                subtitle_count = subtitle_count + 1

            elif is_subtitle_directory(subentry):
                extract_clean_subtitles(
                    entry,
                    subentry,
                    subtitle_count,
                    clean_dirname
                )

            elif os.path.isdir(subentry):
                rmtree(subentry)

            else:
                os.remove(subentry)

        os.rename(entry, (directory / clean_dirname))


def main():
    """Takes a CLI directory argument and cleans the provided directory"""

    parser = argparse.ArgumentParser(
        prog="JellyClean",
        description="A CLI tool for cleaning up a Jellyfin media directory",
    )
    parser.add_argument("directory", type=Path, help="Directory to clean")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        raise ValueError(f"{args.directory} is not a directory")

    clean_dir(args.directory)


if __name__ == "__main__":
    main()
