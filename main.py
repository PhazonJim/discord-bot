import asyncio
import os

from dotenv import load_dotenv

from bots import BIG_TUNA

load_dotenv(override=True)
TOKEN = os.environ.get("DISCORD_TOKEN")


async def main():
    await BIG_TUNA.start(TOKEN)


asyncio.run(main())
