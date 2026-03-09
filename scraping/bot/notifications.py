from scraping.models import ProductInfo
from scraping.bot.telegram import send_message


def _format_product_list(products: list[ProductInfo], category: str) -> str:
    lines = [f"🟢 *Scraping finished — {category}* ({len(products)} products)\n"]

    for product in products[:10]:
        prices_str = f"${product.price}" if product.price else "N/A"

        lines.append(f"• {product.product_name} — *{prices_str}*")
    if len(products) > 10:
        lines.append(f"_...and more {len(products) - 10} products_")

    return "\n".join(lines)


async def notify_success(products: list[ProductInfo], category: str) -> None:
    message = _format_product_list(products, category)

    await send_message(message)

    return None


async def notify_error(category: str, reason: str) -> None:
    message = f"🔴 *Scraping error — {category}*\n{reason}"

    await send_message(message)

    return None
