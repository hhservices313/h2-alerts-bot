import json
import asyncio
import aiohttp
from checker import check_product
from utils.notify import send_discord_webhook

# Load products from trackers.json
with open("trackers.json", "r") as f:
    CONFIG = json.load(f)

PRODUCTS = CONFIG.get("products", [])
CHECK_INTERVAL = 30  # seconds delay between loops


async def monitor_loop():
    print("🔄 H2 Alerts Bot Started... Monitoring products!")

    async with aiohttp.ClientSession() as session:
        while True:
            for product in PRODUCTS:
                try:
                    print(f"🔎 Checking: {product['name']}")

                    in_stock = await check_product(session, product)

                    if in_stock:
                        message = f"✅ **IN STOCK!**\n{product['name']}\n{product['url']}"
                        print(message)

                        # Send Discord alert
                        webhook_env = product.get("channel_env", "WEBHOOK_DEFAULT")
                        webhook_url = os.getenv(webhook_env)

                        await send_discord_webhook(webhook_url, message)

                except Exception as e:
                    print(f"❌ Error checking {product['name']}: {e}")

            await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        asyncio.run(monitor_loop())
    except KeyboardInterrupt:
        print("🛑 Bot stopped manually.")
