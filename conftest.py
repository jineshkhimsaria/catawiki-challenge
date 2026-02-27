import os
import platform
import shutil
from typing import Optional

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config import IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT

CHROME_BINARY = os.environ.get("CHROME_BINARY", "")
CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH", "")
DEFAULT_BROWSER = os.environ.get("BROWSER", "chrome")


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: core smoke tests")
    config.addinivalue_line("markers", "search: search-related tests")
    config.addinivalue_line("markers", "localization: localization / i18n tests")
    config.addinivalue_line("markers", "homepage: homepage validation tests")
    config.addinivalue_line("markers", "lotpage: lot detail page tests")
    config.addinivalue_line("markers", "category: category search tests")
    config.addinivalue_line("markers", "edge: edge case tests")


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=DEFAULT_BROWSER,
        help="Browser to run tests: chrome, firefox",
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed (visible) mode",
    )


def _find_chrome_binary() -> str:
    if CHROME_BINARY and os.path.isfile(CHROME_BINARY):
        return CHROME_BINARY
    candidates = [
        "/opt/google/chrome/chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    found = (
        shutil.which("google-chrome")
        or shutil.which("google-chrome-stable")
        or shutil.which("chromium-browser")
    )
    return found or ""


def _find_chromedriver() -> str:
    if CHROMEDRIVER_PATH and os.path.isfile(CHROMEDRIVER_PATH):
        return CHROMEDRIVER_PATH
    try:
        return ChromeDriverManager().install()
    except Exception:
        return ""


def _get_chromedriver_service() -> ChromeService:
    path = _find_chromedriver()
    if path:
        return ChromeService(path)
    return ChromeService()


def _apply_stealth(options: ChromeOptions) -> None:
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,900")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)


def _inject_stealth_js(driver: webdriver.Chrome) -> None:
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"},
    )


def _create_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    options = ChromeOptions()
    binary = _find_chrome_binary()
    if binary:
        options.binary_location = binary
    if headless:
        options.add_argument("--headless=new")
    _apply_stealth(options)
    service = _get_chromedriver_service()
    driver = webdriver.Chrome(service=service, options=options)
    _inject_stealth_js(driver)
    return driver


def _create_firefox_driver(headless: bool = True) -> webdriver.Firefox:
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    )
    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()
    headed = request.config.getoption("--headed")
    headless = not headed

    if browser == "chrome":
        drv = _create_chrome_driver(headless=headless)
    elif browser == "firefox":
        drv = _create_firefox_driver(headless=headless)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    drv.implicitly_wait(IMPLICIT_WAIT)
    drv.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    yield drv

    drv.quit()
