import asyncio
import os

from dotenv import load_dotenv

load_dotenv(override=True)

from bots import BIG_TUNA

TOKEN = os.environ.get("DISCORD_TOKEN")


async def main():
    await BIG_TUNA.start(TOKEN)


asyncio.run(main())
