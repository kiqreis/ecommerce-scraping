BASE_URL = "https://webscraper.io/test-sites/e-commerce/allinone"
DB_NAME = "prices.db"
MAX_PRODUCTS_CATEGORY = 100
MAX_CONCURRENT_REQUEST = 3
FETCH_RETRIES = 4
FETCH_BASE_DELAY = 2.0
BACKOFF_CAP = 60.0

COMMON_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}
