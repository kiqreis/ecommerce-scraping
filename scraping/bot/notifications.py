from scraping.models import ProductInfo
from scraping.bot.telegram import send_message


def _format_product_list(products: list[ProductInfo], category: str) -> str:
    lines = [f"🟢 <b>Scraping finished in {category}</b> ({len(products)} products)\n"]

    for product in products[:10]:
        price_str = f"${product.price}" if product.price else "N/A"
        link = f'<a href="{product.url}">{product.product_name}</a>'
        lines.append(f"• {link}: <b>{price_str}</b>")

    if len(products) > 10:
        lines.append(f"<i>...and more {len(products) - 10} products</i>")

    return "\n".join(lines)


async def notify_price_changes(changes: list[dict]) -> None:
    if not changes:
        return

    lines = ["<b>Variações de preço detectadas</b>\n"]
    for c in changes:
        arrow = "📈" if c["pct_change"] > 0 else "📉"
        link = f'<a href="{c["url"]}">{c["product_name"]}</a>'
        lines.append(
            f"{arrow} {link}\n"
            f"   <s>${c['old_price']}</s> → <b>${c['new_price']}</b> "
            f"({c['pct_change']:+.1f}%)"
        )

    await send_message("\n".join(lines))


async def notify_success(products: list[ProductInfo], category: str) -> None:
    message = _format_product_list(products, category)

    await send_message(message)

    return None


async def notify_error(category: str, reason: str) -> None:
    message = f"🔴 *Scraping error — {category}*\n{reason}"

    await send_message(message)

    return None
