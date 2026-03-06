import logging
import sqlite3
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


def get_max_price(
    connection: sqlite3.Connection, category: str
) -> tuple[Optional[int], Optional[str]]:
    cursor = connection.execute(
        """
        SELECT price, timestamp
        FROM products
        WHERE category = ?
        ORDER BY price DESC
        LIMIT 1
        """,
        (category,),
    )

    result = cursor.fetchone()

    return (result[0], result[1]) if result else (None, None)


def price_variation(connection: sqlite3.Connection, category: str) -> pd.DataFrame:
    df = pd.read_sql(
        "SELECT product_name, price, timestamp FROM products WHERE category = ?",
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


def price_summary(connection: sqlite3.Connection, category: str) -> pd.DataFrame:
    df = pd.read_sql(
        "SELECT product_name, price FROM products WHERE category = ?",
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
