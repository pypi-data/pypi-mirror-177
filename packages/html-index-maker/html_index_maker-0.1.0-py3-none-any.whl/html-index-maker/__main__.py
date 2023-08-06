from argparse import ArgumentParser
from pathlib import Path
import json

from .driver import get_driver
from .scraper import scrape


class Arguments:
    filepath: str
    outpath: str


def scrape_files(path: Path) -> list:
    driver = get_driver()
    if not path.is_dir():
        return [scrape(driver, path)]
    return [scrape(driver, filepath) for filepath in path.glob("**/*.html")]


def main(argv: Arguments):
    data = scrape_files(Path(argv.filepath).resolve())
    with open(Path(argv.outpath).resolve(), "w") as json_file:
        json_file.write(json.dumps(data, indent=2))


if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("filepath", help="File path or directory to scrape.")
    args.add_argument("--outpath", help="Output JSON file path.", default="./data.json")
    main(args.parse_args())
