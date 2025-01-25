import re


def clean(og_name: str) -> str:
    """Check if file or directory name is valid and reformat if not"""

    if not valid(og_name):
        new_name: str = reformat(og_name)

        if not valid(new_name):
            error_message = "Could not validate entry name after reformat"
            raise ValueError(f"{error_message}:\n{og_name} -> {new_name}")

        return new_name

    return og_name


def valid(entry: str) -> bool:
    """Check if file or directory name is in valid format

    Example:
        Happy.Gilmore.1996
        Happy.Gilmore.1996.mkv
    """
    return re.match(r"^(\w+\.)+\d{4}(.mkv|.mp4)?$", entry) is not None


def reformat(original_name: str) -> str:
    """Reformat file and directory names to dot-separated movie title and release year

    Example:
        Happy.Gilmore.1996
        Happy.Gilmore.1996.mkv
    """

    cleaned_name: str = re.sub(r"\s", ".", original_name)
    cleaned_name: str = re.sub(r"[\(\)]", "", cleaned_name)

    cutoff: int = 0
    for year_match in re.finditer(r"(?<=.)\b(?:19|20)\d{2}\b", cleaned_name):
        cutoff = year_match.end()

    ext_match: re.Match[str] | None = re.search(r"(.mkv|.mp4)", original_name)
    if ext_match:
        return cleaned_name[:cutoff] + ext_match.group()

    return cleaned_name[:cutoff]
