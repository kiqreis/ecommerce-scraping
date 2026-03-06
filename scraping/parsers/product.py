import logging
from typing import Optional

from bs4 import BeautifulSoup
from scraping.models import ProductInfo

logger = logging.getLogger(__name__)


def _parse_price(prices: int, index: int) -> Optional[int]:
    try:
        txt = prices[index].get_index(strip=True)
        txt = txt.replace("$", "").replace(",", "").strip()

        return int(float(txt))
    except (IndexError, ValueError):
        return None


def parse_product(html: str, category: str, url: str) -> Optional[ProductInfo]:
    soup = BeautifulSoup(html)

    try:
        title = soup.find("h4", class_="title")

        if not title:
            logger.debug(f"Title not found in {url}")
            return None

        prices = soup.find_all(attrs={"itemprop": "price"})

        return ProductInfo(
            product_name=title.get_text(strip=True),
            price=_parse_price(prices, 0),
            category=category,
            url=url,
        )

    except Exception as error:
        logger.warning(f"Unexpected error when parsing {url}: {error}")
        return None
