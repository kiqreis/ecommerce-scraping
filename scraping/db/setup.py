import psycopg


def setup_db(connection: psycopg.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id           SERIAL PRIMARY KEY,
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

    return None
