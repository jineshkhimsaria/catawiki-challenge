import pytest

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from config import CATEGORY_KEYWORDS

@pytest.mark.search
@pytest.mark.category
class TestCategorySearch:

    @pytest.mark.parametrize("keyword", CATEGORY_KEYWORDS)

    def test_search_returns_results_for_category(self, driver, keyword):
        home = HomePage(driver)
        home.navigate()
        home.search_for(keyword)

        results = SearchResultsPage(driver)
        assert results.is_search_results_page(), (
            f"Expected search results page for '{keyword}', got: {driver.current_url}"
        )
        cards = results.get_lot_cards()
        assert len(cards) >= 1, (
            f"Expected at least 1 result for '{keyword}', found {len(cards)}"
        )