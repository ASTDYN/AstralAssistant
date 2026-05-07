import aiohttp
from bs4 import BeautifulSoup

RSI_PROFILE_URL = "https://robertsspaceindustries.com/citizens/{handle}"
_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AstralBot/1.0)"}


async def check_verification_code(handle: str, code: str) -> bool:
    url = RSI_PROFILE_URL.format(handle=handle)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers=_HEADERS, timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                if resp.status != 200:
                    return False
                html = await resp.text()

        soup = BeautifulSoup(html, "html.parser")
        page_text = soup.get_text()
        return code.upper() in page_text.upper()

    except Exception:
        return False
