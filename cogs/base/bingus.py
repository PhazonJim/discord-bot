from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from discord.ext import commands
import os
from cogs.base.errors import TimeOutException
from db import LOCAL_DATABASE

if TYPE_CHECKING:
    import dataset


async def setup(bot: commands.Bot):
    await bot.add_cog(Bingus(bot))


class Bingus(commands.Cog):
    """Base Bingus Class"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.botspam_channel_id = int(os.environ.get("BOTSPAM_CHANNEL_ID"))
        self.user_table: dataset.Table = LOCAL_DATABASE["user_data"]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bingus is Ready!")

    async def _bingus_error(self, ctx: commands.Context, error):
        print(error)
        message = "Oopsie whoopsie! Something broke :("
        if isinstance(error, commands.CommandOnCooldown):
            message = f"You absolute dingus, you have {round(error.retry_after, 2)} seconds left on your cooldown."
            await ctx.send(message, ephemeral=True, delete_after=20)
        elif isinstance(error, TimeOutException):
            seconds_left = increase_timeout(ctx.author.id)
            message = f"Using commands while in timeout has earned you 60 more seconds on your timeout {ctx.author.mention} - you have {seconds_left} seconds left."
            await ctx.send(message)
        else:
            await ctx.send(message, delete_after=5.0)


def author_in_timeout(user_id: int) -> bool:
    user_table: dataset.Table = LOCAL_DATABASE["user_data"]
    user = user_table.find_one(user_id=user_id)
    if not user:
        return False
    timeout_until = user.get("timeout_until", 0)
    if not timeout_until:
        return False
    if datetime.now() > timeout_until:
        return False
    return True

def increase_timeout(user_id: int):
    user_table: dataset.Table = LOCAL_DATABASE["user_data"]
    user = user_table.find_one(user_id=user_id)
    if user:
        timeout_until = user.get("timeout_until", 0)
    if timeout_until:
        new_timeout = timeout_until + timedelta(seconds=60)
        user_table.update(dict(user_id=user_id, timeout_until=new_timeout), ["user_id"])
        return (new_timeout - datetime.now()).seconds

def punish_timeouts():
    async def check_timeout(ctx: commands.Context):
        if author_in_timeout(ctx.author.id):
            raise TimeOutException("User is in timeout!")
        return True

    return commands.check(check_timeout)
