from argparse import ArgumentParser
from pathlib import Path
import json

from .driver import get_driver
from .html import scrape_html
from .markdown import make_markdown
from .org import read_org, make_org


class Arguments:
    input: str
    output: str
    format: str


def scrape_files(path: Path, format: str) -> list:
    if format == ".org":
        func = lambda x: read_org(x)
    elif format == ".html":
        driver = get_driver()
        func = lambda x: scrape_html(driver, x)
    if not path.is_dir():
        return [func(path)]
    return [func(file) for file in path.glob(f"**/*{format}")]


def main(argv: Arguments):
    data = scrape_files(Path(argv.input).resolve(), argv.format)
    data.sort(key=lambda x: x["file"])
    filepath = Path(argv.output)
    with open(filepath.resolve(), "w") as file:
        if filepath.suffix == ".json":
            file.write(json.dumps(data, indent=2))
        elif filepath.suffix == ".js":
            file.write(f"let indexData = {json.dumps(data, indent=2)}")
        elif filepath.suffix == ".md":
            file.write(f"{make_markdown(data)}")
        elif filepath.suffix == ".org":
            file.write(f"{make_org(data)}")


if __name__ == "__main__":
    default_input = "."
    default_output = "./data.json"
    default_format = ".html"

    args = ArgumentParser(
        prog="Index scraper",
        usage=f"python -m html-index-scraper -i {default_input} -o {default_output} -f {default_format}",
    )
    args.add_argument(
        "-i", "--input", help="File or directory to scrape.", default=default_input
    )
    args.add_argument(
        "-o",
        "--output",
        help="Output file path, .json, .js, .html, .md",
        default=default_output,
    )
    args.add_argument(
        "-f",
        "--format",
        help="Input file format, .html, .org, .md",
        default=default_format,
    )
    main(args.parse_args())
