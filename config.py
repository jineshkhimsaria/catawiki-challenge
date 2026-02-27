import os

BASE_URL = os.environ.get("BASE_URL", "https://www.catawiki.com")
HOME_PATH = "/en/"
SEARCH_KEYWORD = os.environ.get("SEARCH_KEYWORD", "train")
IMPLICIT_WAIT = int(os.environ.get("IMPLICIT_WAIT", "10"))
PAGE_LOAD_TIMEOUT = int(os.environ.get("PAGE_LOAD_TIMEOUT", "30"))

LOCALES = {
    "en": "/en/",
    "nl": "/nl/",
    "de": "/de/",
    "fr": "/fr/",
    "it": "/it/",
    "es": "/es/",
}

CATEGORY_KEYWORDS = ["painting", "rolex watch", "silver coin", "diamond ring"]