import json
import asyncio
from utils.fetch import fetch_text
from utils.notify import send_discord_webhook


async def check_product(session, product):
    """Returns True if product appears in stock, False if not."""
    html = await fetch_text(session, product["url"])
    html_lower = html.lower()

    # Basic generic checks for "in stock" phrases
    possible_indicators = [
        "add to cart",
        "in stock",
        "available",
        "ship",
        "\"availability\":\"in_stock\"",
        "pick up",
    ]

    for phrase in possible_indicators:
        if phrase in html_lower:
            return True

    return False


async def run_all_checks(products):
    """Checks all products and returns a list of products that are in stock."""
    import aiohttp

    results = []

    async with aiohttp.ClientSession() as session:
        tasks = [check_product(session, p) for p in products]
        statuses = await asyncio.gather(*tasks)

    for product, status in zip(products, statuses):
        if status:
            results.append(product)

    return results
