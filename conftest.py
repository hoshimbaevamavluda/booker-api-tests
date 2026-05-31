import pytest
from playwright.sync_api import sync_playwright
from api.api_client import PlaywrightBookerAPI  # импортируй свой класс


@pytest.fixture(scope="session")
def api_base_url():
    """Базовый URL для Restful Booker"""
    return "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def restful_client(api_base_url):
    """Фикстура для PlaywrightBookerAPI"""
    with sync_playwright() as p:
        context = p.request.new_context(base_url=api_base_url)
        client = PlaywrightBookerAPI(context, base_url=api_base_url)
        yield client
        context.dispose()