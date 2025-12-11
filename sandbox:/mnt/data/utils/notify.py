import os
import aiohttp
import asyncio

WEBHOOK_TIMEOUT = int(os.getenv("WEBHOOK_TIMEOUT", 15))


async def send_discord_webhook(webhook_url: str, message: str):
    if not webhook_url:
        print("❌ Missing webhook URL, skipping notification.")
        return

    payload = {"content": message}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                webhook_url, json=payload, timeout=WEBHOOK_TIMEOUT
            ) as resp:
                if resp.status not in (200, 204):
                    print(f"⚠️ Webhook error {resp.status}: {await resp.text()}")
        except Exception as e:
            print(f"❌ Webhook failed: {e}")
