import os

import discord
import requests
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands, tasks

from models import REGISTRY, Check

TEST_GUILD_ID = int(os.environ.get("TEST_GUILD_ID"))
ARCHIPELAGO_GUILD_ID = int(os.environ.get("ARCHIPELAGO_GUILD_ID"))
CHECKS_CHANNEL_ID = int(os.environ.get("CHECKS_CHANNEL_ID"))

async def setup(bot: commands.Bot):
    await bot.add_cog(Archipelago(bot))


class Archipelago(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.get_latest_info.start()
        self.tracker_url = "https://archipelago.gg/sphere_tracker/wWv6vLGGQ9yOyB9ZzbUB9A" #TODO Automatically grab this somehow. 
        self.init = True

    def cog_unload(self):
        self.get_latest_info.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is connected to the following guild(s):\n")
        for guild in self.bot.guilds:
            print(f"{guild.name}(id: {guild.id})")

    @tasks.loop(seconds=120)
    async def get_latest_info(self):
        if self.init:
            self.init = False
            return
        print("Fetching latest archipelago info...")
        new_checks = []
        payload = requests.get(self.tracker_url)
        soup = BeautifulSoup(payload.content, "html.parser")
        table_rows = soup.find("tbody").find_all("tr")
        for row in table_rows:
            cells = row.find_all("td")
            cells_by_text = [cell.get_text() for cell in cells]
            sphere, finder, receiver, item, location, game = cells_by_text
            check = Check(
                sphere=sphere,
                finder=finder,
                receiver=receiver,
                item=item,
                location=location,
                game=game,
            )
            is_new_check = REGISTRY.add_check(check=check)
            if is_new_check:
                new_checks.append(check)
        if new_checks:
            await self.handle_new_checks(new_checks)
        print("Done!")

    async def handle_new_checks(self, new_checks: list[Check]) -> None:
        if new_checks:
            channel = self.bot.get_channel(CHECKS_CHANNEL_ID)
            new_checks.sort(key=lambda x: x.receiver)
            for check in new_checks:
                message = f"**{check.receiver}** received **{check.item}** from **{check.finder}** (**{check.location}**)"
                print(message)
                await channel.send(message)

    @app_commands.command()
    @app_commands.guilds(ARCHIPELAGO_GUILD_ID, TEST_GUILD_ID)
    @app_commands.describe(player="Player")
    async def check_player(self, interaction: discord.Interaction, player: str):
        checks = REGISTRY.get_checks_for_player(player)
        message = f"Checks found for player: {player}\n"
        for check in checks:
            message += f"{check.item}\n"
        await self.send_big_message(interaction=interaction, message=message)

    @app_commands.command()
    @app_commands.guilds(ARCHIPELAGO_GUILD_ID, TEST_GUILD_ID)
    async def all_checks(self, interaction: discord.Interaction):
        message = "Checks found for all players:\n"
        for check in REGISTRY.checks:
            message_chunk = f"{check.receiver}: {check.item}\n"
            message += message_chunk
        await self.send_big_message(interaction=interaction, message=message)

    async def send_big_message(self, interaction: discord.Interaction, message: str):
        split_message = ""
        followup = False
        split_messages = message.strip().split("\n")
        for idx, line in enumerate(split_messages):
            if len(split_message + line) >= 2000:
                if followup:
                    await interaction.followup.send(content=split_message)
                else:
                    await interaction.response.send_message(content=split_message)
                    followup = True
                split_message = ""
            split_message += line + "\n"
            if idx == len(split_messages) - 1:
                if followup:
                    await interaction.followup.send(content=split_message)
                else:
                    await interaction.response.send_message(content=split_message)
                    followup = True
