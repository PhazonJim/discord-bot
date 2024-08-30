import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


BIG_TUNA = commands.Bot(
    command_prefix="$",
    description="Big Tuna!",
    intents=intents,
)


@BIG_TUNA.tree.command()
@commands.is_owner()
async def sync(interaction: discord.Interaction):
    print("Sync requested...")
    if interaction.user.id == 595294163168395265:
        await BIG_TUNA.tree.sync()
        print("Command tree synced.")
        await interaction.response.send_message("Sync'd!")
    else:
        await interaction.response.send_message("You must be the owner to use this command!")


@BIG_TUNA.tree.command()
@commands.is_owner()
async def reload_cogs(interaction: discord.Interaction):
    print("Cog reload requested...")
    if interaction.user.id == 595294163168395265:
        await BIG_TUNA.reload_extension("cogs.archipelago")
        await BIG_TUNA.reload_extension("cogs.counter")
        await BIG_TUNA.reload_extension("cogs.gamble")
        await BIG_TUNA.reload_extension("cogs.lootbox")
        print("Cogs Reloaded")
        await interaction.response.send_message("Cogs reloaded!")
    else:
        await interaction.response.send_message("You must be the owner to use this command!")


@BIG_TUNA.event
async def setup_hook() -> None:
    print("Setup...")
    await BIG_TUNA.load_extension("cogs.archipelago")
    await BIG_TUNA.load_extension("cogs.counter")
    await BIG_TUNA.load_extension("cogs.gamble")
    await BIG_TUNA.load_extension("cogs.lootbox")
    await BIG_TUNA.tree.sync()
    print("Done setting up...")
