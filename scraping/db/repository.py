import logging
import psycopg

from scraping.models import ProductInfo

logger = logging.getLogger(__name__)


def save_products(connection: psycopg.Connection, products: list[ProductInfo]) -> None:
    if not products:
        logger.info("No products found")
        return None

    rows = [(p.product_name, p.price, p.category, p.url, p.timestamp) for p in products]

    with connection.cursor() as cursor:
        cursor.executemany(
            """
            INSERT INTO products (product_name, price, category, url, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """,
            rows,
        )

    connection.commit()

    logger.info(f"{len(products)} products saved")

    return None
