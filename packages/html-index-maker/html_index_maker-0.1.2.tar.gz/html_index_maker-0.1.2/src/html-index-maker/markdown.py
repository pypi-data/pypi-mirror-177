from pathlib import Path
import re


def read_markdown(filepath: str) -> str:
    pattern = "(#+.*)"
    with open(Path(filepath).resolve(), "r") as file:
        data = re.findall(pattern, file.read())
        print(data)


def make_markdown(data: list) -> str:
    result = "# Index\n"
    for file in data:
        index = [0, 0, 0]
        for header in file["headers"]:
            text = header["text"]
            level = "*" * (int(header["tag"].replace("h", "")) - 1)
            # calculate index
            index = [*index[: len(level)], *[1 for _ in range(len(index) - len(level))]]
            index[len(level) - 1] += 1
            num = "".join(f"{i}." for i in index[: len(level)])
            # get link text
            link = f'[{"&nbsp;"*(len(level)-1)*2} {num} {text}]({file["file"]}#{header["id"]})\n\n'
            result += f"{link}"
    return result
