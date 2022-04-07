# bot.py
import os
import random

import discord
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp
from dotenv import load_dotenv
from db import db
import operations

load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
GUILD = os.environ.get("DISCORD_GUILD")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", description="Simple economy bot")

# @bot.event
# async def on_message(message):
#     guild = discord.utils.get(client.guilds, name=GUILD)
#     if message.author == client.user:
#         return
#     if (
#         message.content.lower().startswith(("who is", "what is"))
#         and message.author.id == 145197613929463808
#     ):
#         await operations.google(message)
#     if message.channel.id in [
#         744081889375027210,
#         293775842532655105,
#         866839494401589332,
#     ]:
#         if message.content.lower().startswith("$bingusbox"):
#             await operations.lootbox(message, client, guild)

@bot.event
async def on_ready():
    print(GUILD)
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )
class Economy(commands.Cog):
  """ All Economy commands """
  @commands.command(
    name="work",
    brief="Work and get some money",
    help="Use this command to work and earn a random amount of money"
  )
  async def _work(self, ctx):
    money = random.randint(1,10)
    await ctx.send(f"{ctx.message.author.mention} worked really hard and earnt {money}!")

if __name__ == "__main__":
    menu = DefaultMenu("◀️", "▶️", "❌")
    bot.help_command = PrettyHelp(menu=menu, color=discord.Colour.green())
    bot.add_cog(Economy(bot))
    bot.run(TOKEN)