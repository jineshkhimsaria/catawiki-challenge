import pytest

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.lot_page import LotPage


@pytest.mark.lotpage
class TestLotDetailsExtended:

    def _navigate_to_first_lot(self, driver, keyword="watch"):
        home = HomePage(driver)
        home.navigate()
        home.search_for(keyword)
        results = SearchResultsPage(driver)
        assert results.is_search_results_page()
        cards = results.get_lot_cards()
        assert len(cards) >= 1
        href = cards[0].get_attribute("href")
        if href:
            driver.get(href)
        else:
            cards[0].click()

    def test_lot_has_breadcrumb(self, driver):
        self._navigate_to_first_lot(driver)
        text = driver.execute_script(
            "var el = document.querySelector('[data-testid=\"breadcrumb-text\"]');"
            "return el ? el.textContent : '';"
        )
        assert text, "Lot page should display a breadcrumb (lot number)"
        print(f"\n  Breadcrumb: {text}")

    def test_lot_has_bid_status_section(self, driver):
        self._navigate_to_first_lot(driver)
        text = driver.execute_script(
            "var el = document.querySelector('[data-testid=\"lot-bid-status-section\"]');"
            "return el ? el.textContent : '';"
        )
        assert "bid" in text.lower() or "sold" in text.lower(), (
            f"Bid status section should mention bid or sold, got: {text[:100]}"
        )

    def test_lot_has_seller_info(self, driver):
        self._navigate_to_first_lot(driver)
        text = driver.execute_script(
            "var el = document.querySelector('[data-testid=\"odp-new-seller-section\"]');"
            "return el ? el.textContent : '';"
        )
        assert "Sold by" in text or "sold" in text.lower(), (
            f"Seller section should contain seller info, got: {text[:100]}"
        )

    def test_lot_has_shipping_info(self, driver):
        self._navigate_to_first_lot(driver)
        text = driver.execute_script(
            "var el = document.querySelector('[data-testid=\"shipping-fee\"]');"
            "return el ? el.textContent : '';"
        )
        assert text, "Lot page should display shipping fee information"
        print(f"\n  Shipping: {text}")

    def test_lot_has_buyer_protection(self, driver):
        self._navigate_to_first_lot(driver)
        text = driver.execute_script(
            "var el = document.querySelector('[data-testid=\"buyer-protection-statement\"]');"
            "return el ? el.textContent : '';"
        )
        assert "Buyer Protection" in text or "protection" in text.lower(), (
            f"Should show buyer protection, got: {text[:100]}"
        )

    def test_lot_name_not_empty(self, driver):
        self._navigate_to_first_lot(driver)
        lot = LotPage(driver)
        name = lot.get_lot_name()
        assert len(name) > 3, f"Lot name should be meaningful, got: {name}"
        print(f"\n  Lot name: {name}")
