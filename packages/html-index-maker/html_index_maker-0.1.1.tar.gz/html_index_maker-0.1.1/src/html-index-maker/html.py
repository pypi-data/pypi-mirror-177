from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from pathlib import Path
import re


def scrape_html(driver: Chrome, htmlfile: Path) -> dict:
    """Returns a dictionary from the scraped htmlfile."""
    driver.get(f"file://{htmlfile}")
    if driver.page_source is not None:
        return {
            "file": str(htmlfile.relative_to(Path.cwd())),
            "headers": get_headers(driver.page_source),
        }


def get_headers(page_source: str) -> dict:
    """Get all h2 and h3 headers in html page."""
    html = BeautifulSoup(page_source, "html.parser")
    headers = html.find_all(re.compile("^h[2-3]$"))
    data = []
    for header in headers:
        if header is not None:
            id = header.get("id")
            if id is not None:
                data.append({"tag": header.name, "id": id, "text": header.text})
    return data
