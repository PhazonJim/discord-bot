# bot.py
import os

import discord
from dotenv import load_dotenv

import operations

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    guild = discord.utils.get(client.guilds, name=GUILD)
    if message.channel.id in [744081889375027210, 293775842532655105, 866839494401589332]:
        if message.author == client.user:
            return
        if message.content.lower().startswith(('who is','what is')) and message.author.id == 145197613929463808:
            await operations.google(message)
        
        if message.content.lower().startswith("$bingusbox"):
            await operations.lootbox(message, client, guild)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)