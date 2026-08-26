"""Shared pytest fixtures.

The driver fixture is function scoped on purpose. Sharing one browser across
tests makes every failure depend on what ran before it, which turns a red suite
into an archaeology exercise. A fresh browser per test costs a few seconds and
buys independent, diagnosable failures.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://www.saucedemo.com"


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run with a visible browser. Headless is the default so CI works unchanged.",
    )


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def driver(request):
    options = Options()
    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    chrome = webdriver.Chrome(options=options)

    # Explicit waits only. Mixing implicit and explicit waits makes timeouts
    # unpredictable, so the implicit wait is pinned at zero and every lookup
    # goes through the helpers in pages/base_page.py.
    chrome.implicitly_wait(0)

    yield chrome
    chrome.quit()
