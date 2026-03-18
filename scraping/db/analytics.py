import logging
import psycopg
from typing import Optional

import pandas as pd

from scraping.models import ProductInfo

logger = logging.getLogger(__name__)


def get_max_price(
    connection: psycopg.Connection, category: str
) -> tuple[Optional[int], Optional[str]]:
    cursor = connection.execute(
        """
        SELECT price, timestamp
        FROM products
        WHERE category = %s
        ORDER BY price DESC
        LIMIT 1
        """,
        (category,),
    )

    result = cursor.fetchone()

    return (result[0], result[1]) if result else (None, None)


def price_variation(connection: psycopg.Connection, category: str) -> pd.DataFrame:
    df = pd.read_sql(
        "SELECT product_name, price, timestamp FROM products WHERE category = %s",
        connection,
        params=(category,),
    )

    if df.empty:
        logger.info(f"No data for analysis in category {category}")
        return df

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d-%m-%Y %H:%M:%S")
    df.sort_values("timestamp", inplace=True)
    df["pct_change"] = df.groupby("product_name")["price"].pct_change() * 100

    return df


def price_summary(connection: psycopg.Connection, category: str) -> pd.DataFrame:
    df = pd.read_sql(
        "SELECT product_name, price FROM products WHERE category = %s",
        connection,
        params=(category,),
    )

    if df.empty:
        return df

    return (
        df.groupby("product_name")["price"]
        .agg(min_price="min", max_price="max", avg_price="mean")
        .reset_index()
        .sort_values("avg_price", ascending=False)
    )


def detect_price_changes(
    connection: psycopg.Connection,
    products: list[ProductInfo],
    threshold_pct: float = 1.0,
) -> list[dict]:
    if not products:
        return None

    names = [p.product_name for p in products]

    cursor = connection.execute(
        """
        SELECT DISTINCT ON (product_name) product_name, price
        FROM products
        WHERE product_name = ANY(%s)
        ORDER BY product_name, timestamp DESC
        """,
        (names,),
    )

    latest_prices = {row[0]: row[1] for row in cursor.fetchall()}

    changes = []

    for product in products:
        old_price = latest_prices.get(product.product_name)

        if old_price and product.price:
            pct = ((product.price - old_price) / old_price) * 100

            if abs(pct) >= threshold_pct:
                changes.append(
                    "product_name": product.product_name,
                    "url": product.url,
                    "old_price": old_price,
                    "new_price": product.price,
                    "pct_change": pct
                )

    return changes
