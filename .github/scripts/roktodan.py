import asyncio
from datetime import datetime, timezone
import aiohttp

URL = "https://www.roktodan.xyz/api/teams/members"

async def check_api():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            URL,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "*/*",
                "Referer": "https://www.roktodan.xyz/teams"
            }
        ) as resp:
            status = resp.status
            data = await resp.json(content_type=None)
            return status, data


async def main():
    try:
        status, data = await check_api()
    except Exception:
        status, data = None, {}

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if status == 200 and data.get("success") is True:
        msg = f"{now} - API UP (HTTP {status})"
    else:
        msg = f"{now} - API DOWN (HTTP {status})"

    print(msg)

    with open("log.txt", "a") as f:
        f.write(msg + "\n")


try:
    loop = asyncio.get_running_loop()
    loop.create_task(main())
except RuntimeError:
    asyncio.run(main())
