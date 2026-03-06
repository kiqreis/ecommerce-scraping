import sqlite3


def setup_db(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            price        INTEGER,
            category     TEXT,
            url          TEXT,
            timestamp    TIMESTAMP
        )
        """
    )

    connection.execute("CREATE INDEX IF NOT EXISTS idx_category ON products (category)")
    connection.commit()
