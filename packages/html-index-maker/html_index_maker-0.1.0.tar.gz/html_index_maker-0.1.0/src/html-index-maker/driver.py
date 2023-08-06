from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome


def get_driver() -> Chrome:
    """Creates a headless driver with Selenium."""
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)
