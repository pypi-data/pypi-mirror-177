import asyncio
from aiohttp import ClientSession


async def get_app_owner_zelid(app_name) -> str:
    async with ClientSession() as session:
        async with session.get(
            f"https://api.runonflux.io/apps/appowner?appname={app_name}"
        ) as resp:
            # print(resp.status)
            data = await resp.json()
            zelid = data.get("data", "")
    return zelid


print(asyncio.run(get_app_owner_zelid("Cerebro")))
