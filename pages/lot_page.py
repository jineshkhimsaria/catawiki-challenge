import re

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

JS_GET_BID = (
    "var el = document.querySelector('[data-testid=\"lot-bid-status-section\"]');"
    "if(el) return el.textContent; return '';"
)

JS_GET_WATCHING = (
    "var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);"
    "while(walker.nextNode()){"
    "  var t = walker.currentNode.textContent.trim();"
    "  if(t.indexOf('watching') > -1) return t;"
    "}"
    "return '';"
)


class LotPage(BasePage):
    LOT_NAME = (By.CSS_SELECTOR, "main h1")

    def is_lot_page(self) -> bool:
        url = self.get_current_url()
        return "/l/" in url

    def get_lot_name(self) -> str:
        return self.get_text(self.LOT_NAME)

    def get_favourites_count(self) -> str:
        text = self.driver.execute_script(JS_GET_WATCHING)
        if text:
            match = re.search(r"(\d+)\s+other\s+people", text)
            if match:
                return match.group(1)
            digits = "".join(c for c in text if c.isdigit())
            if digits:
                return digits
        return "0"

    def get_current_bid(self) -> str:
        text = self.driver.execute_script(JS_GET_BID)
        if text:
            match = re.search(r"[€$£]\s*[\d,.\s]+", text)
            if match:
                return match.group(0).strip()
            lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
            for i, line in enumerate(lines):
                if "current bid" in line.lower() and i + 1 < len(lines):
                    return lines[i + 1]
        return "N/A"

    def print_lot_details(self) -> dict:
        name = self.get_lot_name()
        favourites = self.get_favourites_count()
        bid = self.get_current_bid()

        print("\n" + "=" * 60)
        print("LOT DETAILS")
        print("=" * 60)
        print(f"  Lot Name:         {name}")
        print(f"  Favourites Count: {favourites}")
        print(f"  Current Bid:      {bid}")
        print("=" * 60 + "\n")

        return {"name": name, "favourites": favourites, "current_bid": bid}
