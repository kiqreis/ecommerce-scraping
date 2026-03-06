import asyncio
import logging
import random
from typing import Optional

import httpx

from scraping.config import FETCH_RETRIES, FETCH_BASE_DELAY, BACKOFF_CAP, COMMON_HEADERS
from scraping.fetcher.headers import get_headers, is_blocked


logger = logging.getLogger(__name__)


def _calc_backoff(attempt: int, base_delay: float = FETCH_BASE_DELAY) -> float:
    return random.uniform(0, min(BACKOFF_CAP, base_delay * (2**attempt)))


async def fetch_page(
    client: httpx.AsyncClient,
    url: str,
    retries: int = FETCH_RETRIES,
    base_delay: float = FETCH_BASE_DELAY,
) -> Optional[str]:
    for attempt in range(retries):
        try:
            if attempt > 0:
                wait = _calc_backoff(attempt, base_delay)

                logger.debug(
                    f"Waiting for {wait:.1f}s before trying {attempt + 1} / {retries}"
                )

                await asyncio.sleep(wait)

            logger.debug(f"[attempt {attempt + 1} / {retries}] GET {url}")

            response = await client.get(url, headers=get_headers())

            if response.status_code == 429:
                wait = int(response.headers.get("Retry-After", 0)) or _calc_backoff(
                    attempt, base_delay
                )

                logger.warning(f"Rate limit at {url}. Waiting for {wait:.1f}s")

                await asyncio.sleep(wait)
                continue

            if response.status_code == 403:
                wait = int(response.headers.get("Retry-After", 0))

                logger.warning(f"Access denied on {url}. Waiting for {wait:.1f}s")

                await asyncio.sleep(wait)
                continue

            response.raise_for_status()

            if is_blocked(response.text):
                wait = _calc_backoff(attempt, base_delay)

                logger.warning(f"Block detected on {url}. Trying again on {wait:.1f}s")

                await asyncio.sleep(wait)
                continue

        except httpx.RequestError as error:
            wait = _calc_backoff(attempt, base_delay)

            logger.warning(f"Connection error: {error}. Next attempt in {wait:.1f}")

            await asyncio.sleep(wait)

    logger.error(f"Definitive failure after {retries} attempts: {url}")
    return None


async def bounded_fetch(
    client: httpx.AsyncClient, semaphore: asyncio.Semaphore, url: str
) -> Optional[str]:
    async with semaphore:
        return await fetch_page(client, url)
