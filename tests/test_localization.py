import pytest

from pages.home_page import HomePage
from config import LOCALES


@pytest.mark.localization
class TestLocalization:

    def test_dutch_page_title(self, driver):
        home = HomePage(driver)
        home.navigate(locale_path=LOCALES["nl"])
        title = home.get_page_title()
        assert "veiling" in title.lower(), (
            f"Dutch title should contain 'veiling', got: {title}"
        )

    def test_dutch_search_placeholder(self, driver):
        home = HomePage(driver)
        home.navigate(locale_path=LOCALES["nl"])
        placeholder = home.get_search_placeholder()
        assert "Zoeken" in placeholder, (
            f"Dutch placeholder should contain 'Zoeken', got: {placeholder}"
        )

    def test_dutch_navigation_text(self, driver):
        home = HomePage(driver)
        home.navigate(locale_path=LOCALES["nl"])
        how_it_works = home.get_how_it_works_text()
        help_text = home.get_help_text()
        assert how_it_works == "Zo werkt het", (
            f"Expected 'Zo werkt het', got: {how_it_works}"
        )
        assert help_text == "Hulp", (
            f"Expected 'Hulp', got: {help_text}"
        )

    def test_dutch_category_tabs(self, driver):
        home = HomePage(driver)
        home.navigate(locale_path=LOCALES["nl"])
        tabs = home.get_category_tab_names()
        expected = ["Deze week", "Kunst", "Horloges", "Sieraden"]
        for expected_tab in expected:
            assert any(expected_tab in t for t in tabs), (
                f"Dutch tab '{expected_tab}' not found in: {tabs}"
            )

    def test_english_vs_dutch_title_differs(self, driver):
        home = HomePage(driver)
        home.navigate(locale_path=LOCALES["en"])
        en_title = home.get_page_title()
        home.navigate(locale_path=LOCALES["nl"])
        nl_title = home.get_page_title()
        assert en_title != nl_title, (
            f"English and Dutch titles should differ: en={en_title}, nl={nl_title}"
        )
