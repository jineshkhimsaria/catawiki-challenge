import json

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from config import BASE_URL, HOME_PATH

COOKIE_ACCEPT_LABELS = ["Agree", "Akkoord", "Zustimmen", "Accepter", "Accetta", "Aceptar"]

JS_DISMISS_SIGNUP = (
    "var el = document.querySelector("
    "'div[class*=\"popup\"] svg, div[class*=\"modal\"] button[aria-label=\"Close\"]');"
    "if(el) el.click();"
)


class HomePage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[type="search"]')
    COOKIE_OVERLAY = (By.CSS_SELECTOR, 'div[class*="CookiesBar_overlay"]')
    HOW_IT_WORKS = (By.CSS_SELECTOR, '[data-testid="header-how-it-works-button"]')
    HELP_BUTTON = (By.CSS_SELECTOR, '[data-testid="header-help-button"]')
    CATEGORY_TABS = (By.CSS_SELECTOR, 'button[class*="Tab_template"]')

    def navigate(self, locale_path: str = HOME_PATH) -> None:
        self.driver.get(BASE_URL + locale_path)
        self.dismiss_cookie_banner()
        self.dismiss_signup_popup()

    def dismiss_cookie_banner(self) -> None:
        labels_json = json.dumps(COOKIE_ACCEPT_LABELS)
        js = (
            "var aside = document.querySelector('aside[class*=\"CookiesBar\"]');"
            "if(aside){"
            "  var labels = " + labels_json + ";"
            "  var btns = aside.querySelectorAll('button');"
            "  for(var i=0;i<btns.length;i++){"
            "    var t = btns[i].textContent.trim();"
            "    if(labels.indexOf(t) > -1){btns[i].click(); return true;}"
            "  }"
            "}"
            "return false;"
        )
        clicked = self.driver.execute_script(js)
        if clicked:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located(self.COOKIE_OVERLAY)
                )
            except Exception:
                pass

    def dismiss_signup_popup(self) -> None:
        self.driver.execute_script(JS_DISMISS_SIGNUP)

    def get_page_title(self) -> str:
        return self.driver.title

    def get_search_placeholder(self) -> str:
        return self.driver.execute_script(
            "var el = document.querySelector('input[type=\"search\"]');"
            "return el ? el.placeholder : '';"
        )

    def get_category_tab_names(self) -> list[str]:
        tabs = self.driver.find_elements(*self.CATEGORY_TABS)
        return [t.text.strip() for t in tabs if t.text.strip()]

    def get_how_it_works_text(self) -> str:
        return self.get_text(self.HOW_IT_WORKS)

    def get_help_text(self) -> str:
        return self.get_text(self.HELP_BUTTON)

    def is_search_input_visible(self) -> bool:
        return self.is_visible(self.SEARCH_INPUT)

    def search_for(self, keyword: str) -> None:
        search_input = self.find_clickable(self.SEARCH_INPUT)
        search_input.click()
        search_input.clear()
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.RETURN)
