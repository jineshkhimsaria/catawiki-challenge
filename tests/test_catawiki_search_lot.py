import pytest

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.lot_page import LotPage
from config import SEARCH_KEYWORD


@pytest.mark.smoke
@pytest.mark.search
class TestCatawikiSearchLot:

    def test_search_and_view_lot_details(self, driver):
        home = HomePage(driver)
        home.navigate()

        home.search_for(SEARCH_KEYWORD)

        results = SearchResultsPage(driver)
        assert results.is_search_results_page(), (
            f"Expected search results page, got: {driver.current_url}"
        )

        lot_cards = results.get_lot_cards()
        assert len(lot_cards) >= 2, (
            f"Expected at least 2 lot cards, found {len(lot_cards)}"
        )

        results.click_second_lot()

        lot = LotPage(driver)
        assert lot.is_lot_page(), (
            f"Expected lot detail page (/l/ in URL), got: {driver.current_url}"
        )

        details = lot.print_lot_details()

        print(f"\n  Lot Name: {details['name']}")
        print(f"  Favourites: {details['favourites']}")
        print(f"  Current Bid: {details['current_bid']}")
        assert details["name"], "Lot name should not be empty"
        assert details["favourites"], "Favourites count should not be empty"
        assert details["current_bid"], "Current bid should not be empty"
        