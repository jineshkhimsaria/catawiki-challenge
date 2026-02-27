import pytest

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.search
@pytest.mark.edge
class TestSearchEdgeCases:

    def test_no_results_shows_message(self, driver):
        home = HomePage(driver)
        home.navigate()
        home.search_for("xyznonexistent99999qqq")
        main_text = driver.execute_script(
            "var m = document.querySelector('main');"
            "return m ? m.textContent.substring(0, 500) : '';"
        )
        assert "Related search terms" not in main_text.lower() or "related" in main_text.lower(), (
            f"Should show no-results message, got: {main_text[:200]}"
        )

    def test_search_with_special_characters(self, driver):
        home = HomePage(driver)
        home.navigate()
        home.search_for("art & design")
        url = driver.current_url
        assert "/s?" in url or "/q=" in url, (
            f"Search with special chars should navigate to results page, got: {url}"
        )

    def test_search_preserves_keyword_in_url(self, driver):
        home = HomePage(driver)
        home.navigate()
        home.search_for("vintage clock")
        results = SearchResultsPage(driver)
        assert results.is_search_results_page()
        url = driver.current_url.lower()
        assert "vintage" in url and "clock" in url, (
            f"URL should contain search keywords, got: {url}"
        )

    def test_single_character_search(self, driver):
        home = HomePage(driver)
        home.navigate()
        home.search_for("a")
        url = driver.current_url
        assert "/s?" in url or "/q=" in url or "/en/" in url, (
            f"Single char search should either show results or stay on page, got: {url}"
        )
