import re
from typing import Tuple, List
from steinnews.exceptions import NoChanges, InvalidChanges
from steinnews import patterns


RstFile = str
LatestCotent = str


MAJOR_WORD = "Major"
MINOR_WORD = "Minor"
PATCH_WORD = "Patch"
MAJOR = f"* {MAJOR_WORD}:"
MINOR = f"* {MINOR_WORD}:"
PATCH = f"* {PATCH_WORD}:"
AVAILABLE_LEVELS = [MAJOR, MINOR, PATCH]  # order important


# file_in and file_out may be the same
def write_next_version(file_in, file_out) -> str:
    """Write the next version to the file and return the latest tag"""

    with open(file_in, "r") as file:
        content = file.read()

    output = generate_next_version(content)

    # Write the file out again
    with open(file_out, "w") as file:
        file.write(output)

    return ".".join(get_latest_tag(output))


def get_latest_tag(content) -> Tuple[str, str, str]:
    version_result = re.findall(patterns.VERSION, content, flags=re.M | re.VERBOSE)
    version = version_result[0] if version_result else ("0", "0", "0")
    return version


def generate_next_version(content: RstFile):

    latest_changes, raw_latest_content = get_latest_changes(content)
    # Validate that the bullet points are the same as raw text
    latest_changes_str = changes_to_str(latest_changes)
    if latest_changes_str == "":
        raise NoChanges("No changes found in latest section")

    if latest_changes_str != raw_latest_content:
        res = raw_latest_content.replace(latest_changes_str, "").rstrip("\n")
        res = res.split("\n")
        raise InvalidChanges(res)

    valid_content, highest_level_seen = validate_changes(latest_changes)
    assert len(changes_to_str(valid_content)) == len(
        raw_latest_content
    ), "Latest changes are not valid"
    old_version = get_latest_tag(content)

    # bump version
    version = {
        MAJOR: old_version[0],
        MINOR: old_version[1],
        PATCH: old_version[2],
    }
    found = False
    for key in AVAILABLE_LEVELS:
        if found:
            # making sure to set lower tier version numbers to zero
            version[key] = "0"
        if key == highest_level_seen:
            version[key] = str(int(version[key]) + 1)
            found = True
    new_version_str = version[MAJOR] + "." + version[MINOR] + "." + version[PATCH]

    new_version_underscores = "-" * len(new_version_str)

    # Using re.VERBOSE with re.sub requires workarounds hence not exported in variables
    # Get the latest section, replace it with itself and the new version
    res = re.sub(
        rf"({patterns.LATEST})",
        r"\1* tbd\n\n" + new_version_str + "\n" + new_version_underscores + "\n",
        content,
        flags=re.M,
    )
    return res


def get_latest_changes(content: RstFile):
    # Split the file on the first(most recent) version header
    sections_result = re.split(
        patterns.VERSION, content, flags=re.MULTILINE | re.VERBOSE
    )
    latest_section = sections_result[0]  # if sections_result else content

    # Raw text under the latest version header
    raw_latest_content: LatestCotent = (
        re.compile(patterns.LATEST_TEXT, flags=re.VERBOSE)
        .search(latest_section)
        .group(1)
    )

    validate_bullet_point_format(raw_latest_content)

    # Transform raw text into a list of bullet points
    latest_changes: List[Tuple] = re.findall(
        patterns.CHANGE, raw_latest_content, re.VERBOSE | re.MULTILINE
    )

    return latest_changes, raw_latest_content


def validate_changes(latest_changes: List[Tuple]) -> Tuple[List[tuple], str]:
    seen_level_dict = {
        MAJOR: False,
        MINOR: False,
        PATCH: False,
    }
    valid_changes: List[Tuple] = []
    invalid_changes: List[Tuple] = []

    for change_level, text in latest_changes:
        if change_level not in AVAILABLE_LEVELS:
            invalid_changes.append((change_level + text))
        else:
            seen_level_dict[change_level] = True
            valid_changes.append((change_level, text))

    if invalid_changes:
        raise InvalidChanges(invalid_changes)

    highest_level_seen = (
        MAJOR
        if seen_level_dict[MAJOR]
        else MINOR
        if seen_level_dict[MINOR]
        else PATCH
        if seen_level_dict[PATCH]
        else None
    )
    if highest_level_seen is None:
        raise NoChanges("No changes found in latest section")

    return valid_changes, highest_level_seen


def changes_to_str(changes: List[Tuple[str, str]]) -> str:
    changes_string = ""
    for change_level, text in changes:
        changes_string += change_level + text
    return changes_string


def validate_bullet_point_format(raw_latest_content: str):
    """Make sure that the latest section does not have any line starting from any of the available levels while not being a bullet point"""
    lines = raw_latest_content.split("\n")
    invalid_lines = []
    for line in lines:
        if any(
            line.lstrip().startswith(word)
            for word in [MAJOR_WORD, MINOR_WORD, PATCH_WORD]
        ):
            invalid_lines.append(line)

    if invalid_lines:
        raise InvalidChanges(invalid_lines)
