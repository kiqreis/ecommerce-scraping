import sqlite3
from scraping.config import DB_NAME


def create_connection(db: str = DB_NAME) -> sqlite3.Connection:
    connection = sqlite3.connect(db)
    connection.execute("PRAGMA journal_mode=WAL")

    return connection
