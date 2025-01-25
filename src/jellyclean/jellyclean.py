import logging
import os
from pathlib import Path
from shutil import rmtree

from file_types import FileExtension
from formatting import clean
from subtitles import extract_subtitles, is_subtitle_directory, rename_subtitle


logging.basicConfig(format="%(message)s", level=logging.DEBUG)


def process_directory(directory: Path) -> None:
    """Perform cleanup on contents of provided directory"""

    for entry in map(lambda e: Path(directory, e), os.listdir(directory)):
        subtitle_count: int = 1

        if not os.path.isdir(entry):
            # TODO: if just a movie file, reformat and create parent directory
            continue

        logging.info(f"Performing cleanup on {entry}")

        clean_dirname: str = clean(entry.name)

        for subentry in map(lambda e: Path(entry, e), os.listdir(entry)):
            if subentry.name.endswith((FileExtension.MKV, FileExtension.MP4)):
                clean_filename: str = clean(subentry.name)
                os.rename(subentry, Path(entry, clean_filename))

            elif subentry.name.endswith(FileExtension.SRT):
                subtitle_count = rename_subtitle(
                    Path(entry), subentry.name, clean_dirname, subtitle_count
                )

            elif is_subtitle_directory(subentry):
                extract_subtitles(subentry, subtitle_count, subtitle_name=clean_dirname)

            elif os.path.isdir(subentry):
                rmtree(subentry)

            else:
                os.remove(subentry)

        os.rename(entry, Path(directory, clean_dirname))


if __name__ == "__main__":
    entry = Path("test_dir")

    if not os.path.isdir(entry):
        raise ValueError(f"{entry} is not a directory")

    process_directory(entry)
