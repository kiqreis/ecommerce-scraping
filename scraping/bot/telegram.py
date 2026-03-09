import logging
from typing import Optional

import httpx

from scraping.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)


TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


async def send_message(txt: str, chat_id: Optional[str] = None) -> bool:
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram token not set")

        return None

    target = chat_id or TELEGRAM_CHAT_ID
    url = TELEGRAM_API.format(token=TELEGRAM_BOT_TOKEN)

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                url, json={"chat_id": target, "text": txt, "parse_mode": "Markdown"}
            )

            response.raise_for_status()

            return True

    except httpx.HTTPError as error:
        logger.error(f"Telegram error: {error}")

        return False
