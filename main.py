import asyncio
import logging

import httpx

from scraping.config import (
    BASE_URL,
    MAX_CONCURRENT_REQUEST,
    MAX_PRODUCTS_CATEGORY,
    COMMON_HEADERS,
)

from scraping.fetcher.client import fetch_page, bounded_fetch
from scraping.parsers.listing import parse_products_url
from scraping.parsers.product import parse_product
from scraping.db.connection import create_connection
from scraping.db.setup import setup_db
from scraping.db.repository import save_products

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


async def scrape_category(
    client: httpx.AsyncClient,
    category: str,
    category_url: str,
    connection,
    semaphore: asyncio.Semaphore,
) -> None:
    logger.info(f"Starting category: {category}")

    html = await fetch_page(client, category_url)

    if not html:
        logger.warning(f"Category {category} ignored due to listing failure")
        return

    product_urls = parse_products_url(html)

    logger.info(f"{len(product_urls)} products found in {category}")

    urls_to_scrape = product_urls[:MAX_PRODUCTS_CATEGORY]

    pages = await asyncio.gather(
        *[bounded_fetch(client, semaphore, url) for url in urls_to_scrape]
    )

    products = [
        product
        for url, page in zip(urls_to_scrape, pages)
        if page and (product := parse_product(page, category, url))
    ]

    save_products(connection, products)


async def main(categories: dict[str, str]) -> None:
    connection = create_connection()
    setup_db(connection)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUEST)

    async with httpx.AsyncClient(
        headers=COMMON_HEADERS,
        timeout=httpx.Timeout(30.0),
        limits=httpx.Limits(max_connections=5, max_keepalive_connections=5),
        follow_redirects=True,
    ) as client:
        tasks = [
            scrape_category(client, category, url, connection, semaphore)
            for category, url in categories.items()
        ]

        await asyncio.gather(*tasks)

    connection.close()

    logger.info("Scraping finished")


if __name__ == "__main__":
    CATEGORIES = {
        "laptops": f"{BASE_URL}/computers/laptops",
        "tablets": f"{BASE_URL}/computers/tablets",
        "phones": f"{BASE_URL}/phones/touch",
    }

    asyncio.run(main(CATEGORIES))
