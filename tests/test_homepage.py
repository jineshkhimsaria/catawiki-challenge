import pytest

from pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.homepage
class TestHomepage:

    def test_page_title(self, driver):
        home = HomePage(driver)
        home.navigate()
        title = home.get_page_title()
        assert "catawiki" in title.lower() or "auction" in title.lower(), (
            f"Title should reference Catawiki or auctions, got: {title}"
        )

    def test_search_field_visible(self, driver):
        home = HomePage(driver)
        home.navigate()
        assert home.is_search_input_visible(), "Search input should be visible on homepage"

    def test_category_tabs_present(self, driver):
        home = HomePage(driver)
        home.navigate()
        tabs = home.get_category_tab_names()
        assert len(tabs) >= 5, (
            f"Expected at least 5 category tabs, found {len(tabs)}: {tabs}"
        )
        expected = ["Art", "Watches", "Jewellery"]
        for name in expected:
            assert any(name in t for t in tabs), (
                f"Tab '{name}' not found in: {tabs}"
            )

    def test_how_it_works_link(self, driver):
        home = HomePage(driver)
        home.navigate()
        text = home.get_how_it_works_text()
        assert "how it works" in text.lower(), (
            f"Expected 'How it works', got: {text}"
        )

    def test_help_link(self, driver):
        home = HomePage(driver)
        home.navigate()
        text = home.get_help_text()
        assert "help" in text.lower(), f"Expected 'Help', got: {text}"
