import os
import aiohttp
from tenacity import retry, stop_after_attempt, wait_fixed

USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (compatible)")
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", 3))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 20))

HEADERS = {"User-Agent": USER_AGENT}


@retry(stop=stop_after_attempt(RETRY_ATTEMPTS), wait=wait_fixed(2))
async def fetch_text(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT) as resp:
        resp.raise_for_status()
        return await resp.text()
