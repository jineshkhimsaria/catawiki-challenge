from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def find(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator: tuple) -> list[WebElement]:
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def is_visible(self, locator: tuple, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def click(self, locator: tuple) -> None:
        self.find_clickable(locator).click()

    def type_text(self, locator: tuple, text: str) -> None:
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.find_visible(locator).text

    def get_current_url(self) -> str:
        return self.driver.current_url
