## Catawiki Challenge
1. The catawiki challenge test is part of tests/test_catawiki_search_lot.py (tagged as challenge)
2. I have added more tests to the suite. Those tests are visible under tests directory
3. Catawiki-Search-Lot-Automation-Tests.xlsx contains lots of other tests at API & UI level
4. Catawiki_Test_Strategy.pdf contains a very high level test strategy
5. I prompted Devin.ai (an AI agent) with my requirements. For eg. 
   I want to automate a test scenario (mentioned the details explicitly) on catawiki website.
   Add more tests around the website userflow
   Add github yaml, docker file, etc 
   Create more test scenarios looking at the website
6. Devin.ai works quite well 
7. Once Devin.ai is done with its work, it shares the whole suite with me
8. I reviewed the folder structure, code, re-run it on my local before pushing to Git.


# Catawiki Selenium Test Suite

Automated black-box UI test suite for [Catawiki](https://www.catawiki.com) built with Selenium WebDriver (Python), pytest, and the Page Object Model pattern.

## Project Structure

```
catawiki-selenium/
├── config.py                          # Configuration (BASE_URL, timeouts, locales, keywords)
├── conftest.py                        # Pytest fixtures (driver setup, CLI options, markers)
├── requirements.txt                   # Python dependencies
├── Dockerfile                         # Docker image (Chrome + Firefox pre-installed)
├── entrypoint.sh                      # Docker entrypoint with env var support
├── pages/
│   ├── base_page.py                   # Base page object (common Selenium operations)
│   ├── home_page.py                   # Homepage POM (cookie banner, search, navigation)
│   ├── search_results_page.py         # Search results POM (lot cards, result validation)
│   └── lot_page.py                    # Lot detail POM (bid, favourites, lot name extraction)
└── tests/
    ├── test_catawiki_search_lot.py    # Original scenario: search "train", view lot details
    ├── test_homepage.py               # Homepage validation (title, search field, tabs, links)
    ├── test_localization.py           # Dutch localization (title, placeholder, tabs, nav text)
    ├── test_category_search.py        # Multi-category search (art, watches, coins)
    ├── test_lot_details_extended.py   # Lot page critical elements (seller, shipping, bid, breadcrumb)
    └── test_search_edge_cases.py      # Edge cases (no results, special chars, single char)
```

## Test Tags (Markers)

Each test class is tagged with pytest markers. Use `-m` to filter which tests run:

| Tag            | Description                                     | Test File(s)                                          |
|----------------|-------------------------------------------------|-------------------------------------------------------|
| `smoke`        | Core smoke tests (homepage + original scenario) | `test_catawiki_search_lot.py`, `test_homepage.py`     |
| `search`       | All search-related tests                        | `test_catawiki_search_lot.py`, `test_category_search.py`, `test_search_edge_cases.py` |
| `homepage`     | Homepage validation                             | `test_homepage.py`                                    |
| `localization` | Localization / i18n tests                       | `test_localization.py`                                |
| `category`     | Multi-category search tests                     | `test_category_search.py`                             |
| `lotpage`      | Lot detail page tests                           | `test_lot_details_extended.py`                        |
| `edge`         | Edge case / boundary tests                      | `test_search_edge_cases.py`                           |

**Tag examples:**
```bash
pytest tests/ -m smoke                     # Run only smoke tests
pytest tests/ -m "search and not edge"     # Search tests excluding edge cases
pytest tests/ -m "localization or lotpage" # Localization + lot page tests
```

## Running Locally

### Prerequisites

- Python 3.10+
- Chrome or Firefox installed

### Install & Run

```bash
pip install -r requirements.txt

# Run all tests (Chrome headless, default)
pytest tests/ -v --browser=chrome -s

# Run with Firefox
pytest tests/ -v --browser=firefox -s

# Run in headed mode (visible browser)
pytest tests/ -v --browser=chrome --headed -s

# Run specific tag
pytest tests/ -v --browser=chrome -m smoke -s

# Generate HTML report
pytest tests/ -v --browser=chrome -s --html=reports/report.html --self-contained-html
```

### Environment Variables

| Variable          | Default                       | Description                    |
|-------------------|-------------------------------|--------------------------------|
| `BASE_URL`        | `https://www.catawiki.com`    | Target site base URL           |
| `BROWSER`         | `chrome`                      | Default browser for `--browser`|
| `SEARCH_KEYWORD`  | `train`                       | Default search keyword         |
| `CHROME_BINARY`   | (auto-detect)                 | Path to Chrome binary          |
| `CHROMEDRIVER_PATH`| (auto-detect)                | Path to ChromeDriver binary    |
| `IMPLICIT_WAIT`   | `10`                          | Implicit wait timeout (seconds)|
| `PAGE_LOAD_TIMEOUT`| `30`                         | Page load timeout (seconds)    |

## Running with Docker

### Build the image

```bash
docker build -t catawiki-tests .
```

### Run all tests (Chrome, default)

```bash
docker run --rm catawiki-tests
```

### Run with specific browser

```bash
docker run --rm -e BROWSER=chrome catawiki-tests
docker run --rm -e BROWSER=firefox catawiki-tests
```

### Run with specific tags

```bash
docker run --rm -e TAGS=smoke catawiki-tests
docker run --rm -e TAGS="search and not edge" catawiki-tests
docker run --rm -e TAGS=localization catawiki-tests
docker run --rm -e TAGS="smoke or lotpage" catawiki-tests
```

### Run with custom base URL

```bash
docker run --rm -e BASE_URL=https://www.catawiki.com -e BROWSER=chrome -e TAGS=smoke catawiki-tests
```

### Combine all parameters

```bash
docker run --rm \
  -e BASE_URL=https://www.catawiki.com \
  -e BROWSER=firefox \
  -e TAGS="search and category" \
  catawiki-tests
```

### Extract HTML report from container

```bash
docker run --rm -v $(pwd)/reports:/app/reports catawiki-tests
# Report is saved to ./reports/report.html
```

## Cross-Browser Support

| Browser | Flag              | Docker Support | Notes                           |
|---------|-------------------|----------------|---------------------------------|
| Chrome  | `--browser=chrome`| Yes            | Pre-installed in Docker image   |
| Firefox | `--browser=firefox`| Yes           | Pre-installed in Docker image   |

## Test Scenarios (25 total)

1. **Search & View Lot** (1 test) - Search "train", click 2nd lot, extract name/favourites/bid
2. **Homepage** (5 tests) - Title, search field, category tabs, "How it works", Help link
3. **Localization** (5 tests) - Dutch title, placeholder, nav text, category tabs, EN vs NL comparison
4. **Category Search** (4 tests) - Art/Watches/Coins parametrized search + URL validation
5. **Lot Page** (6 tests) - Breadcrumb, bid status, seller info, shipping, buyer protection, lot name
6. **Edge Cases** (4 tests) - No results, special chars, keyword in URL, single char search

## Github Pipeline

1. Runs on every push to the PR
2. It executes smoke tests (tagged as smoke) for now on https://www.catawiki.com otherwise it
   should actually run on url of the feature branch by creating environment variable BASE_URL
3. Test report is available as github artifacts in reports directory