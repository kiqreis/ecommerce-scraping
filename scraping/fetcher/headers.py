import random
from scraping.config import COMMON_HEADERS

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 Safari/605.1.15",
]

BLOCK_SIGNALS = (
    "captcha",
    "g-recaptcha",
    "account-verification",
    "acesso negado",
    "unusual traffic",
    "verificação de segurança",
)


def get_headers() -> dict[str, str]:
    return {**COMMON_HEADERS, "User-Agent": random.choice(USER_AGENTS)}


def is_blocked(html: str) -> bool:
    return any(signal in html.lower() for signal in BLOCK_SIGNALS)
