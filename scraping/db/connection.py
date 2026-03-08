import logging
import psycopg

from scraping.config import DB_CONFIG

logger = logging.getLogger(__name__)


def create_connection(db_config: dict = DB_CONFIG) -> psycopg.Connection:
    return psycopg.connect(**db_config)
