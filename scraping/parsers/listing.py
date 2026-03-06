from bs4 import BeautifulSoup


def parse_products_url(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = soup.select("a.title")

    return [
        (
            f"https://webscraper.io{a['href']}"
            if not a["href"].startswith("http")
            else a["href"]
        )
        for a in urls
        if a.get("href")
    ]
