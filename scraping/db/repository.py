import logging
import sqlite3
from dataclasses import asdict

import pandas as pd

from scraping.models import ProductInfo

logger = logging.getLogger(__name__)


def save_products(connection: sqlite3.Connection, products: list[ProductInfo]) -> None:
    if not products:
        logger.info("No products found")
        return None

    df = pd.DataFrame([asdict(product) for product in products])
    df.to_sql("products", connection, if_exists="append", index=False)

    connection.commit()

    logger.info(f"{len(products)} products saved")

    return None
