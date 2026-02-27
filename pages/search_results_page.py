from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    LOT_CARDS = (By.CSS_SELECTOR, 'main a[href*="/l/"]')
    NO_RESULTS_MESSAGE = (By.CLASS_NAME, 'tw:text-neutral-tertiary')

    def is_search_results_page(self) -> bool:
        url = self.get_current_url()
        return "/s?" in url or "/q=" in url or "search" in url.lower()

    def get_lot_cards(self) -> list:
        return self.find_all(self.LOT_CARDS)

    def click_second_lot(self) -> None:
        lots = self.get_lot_cards()
        if len(lots) < 2:
            raise AssertionError(
                f"Expected at least 2 lots, found {len(lots)}"
            )
        lot = lots[1]
        href = lot.get_attribute("href")
        if href:
            self.driver.get(href)
        else:
            lot.click()
