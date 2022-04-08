# main.py
import os

import discord 
from discord.ext import commands
from dotenv import load_dotenv

from commands.bingusbox import Bingus
from commands.google import google

load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
GUILD = os.environ.get("DISCORD_GUILD")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="~", description="Simple discord bot", intents=intents)

# @bot.event
# async def on_message(message):
#     if (
#         message.content.lower().startswith(("who is", "what is"))
#         and message.author.id == 145197613929463808
#     ):
#         await google(message)

@bot.event
async def on_ready():
    print(GUILD)
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})")

if __name__ == "__main__":
    bot.add_cog(Bingus(bot))
    bot.run(TOKEN)