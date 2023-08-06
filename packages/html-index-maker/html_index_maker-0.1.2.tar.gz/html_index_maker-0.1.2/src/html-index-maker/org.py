from orgparse import load, OrgNode
from pathlib import Path
from typing import List
import re


LEVELS = {
    "*": "h2",
    "**": "h3",
    "***": "h4",
}


def read_org(filepath: Path) -> list:
    root: List[OrgNode] = load(filepath)
    headers = []
    for node in root[1:]:
        header = re.findall(r"(\*+.*)", f"{node}")[0]
        level, text = header.split(" ", 1)
        if len(level) < 3:
            headers.append(
                {
                    "tag": LEVELS[level],
                    "id": node.get_property(key="CUSTOM_ID"),
                    "text": text,
                }
            )
    return {"file": str(filepath.relative_to(Path.cwd())), "headers": headers}


def make_org(data: list) -> str:
    result = "* Index\n"
    for file in data:
        index = [0, 0, 0]
        result += f"** {Path(file['file']).stem.capitalize()}\n\n"
        for header in file["headers"]:
            text = header["text"]
            level = "*" * (int(header["tag"].replace("h", "")) - 1)
            # calculate index
            index = [*index[: len(level)], *[1 for _ in range(len(index) - len(level))]]
            index[len(level) - 1] += 1
            num = "".join(f"{i}." for i in index[: len(level)])
            # get link text
            link = f'{"  "*(len(level)-1)} [[./{file["file"]}::{text}][{num} {text}]]\n\n'
            result += f"{link}"
    return result
