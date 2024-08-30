import pathlib
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

import yaml
from discord.ext import commands

from cogs.base.errors import TimeOutException
from db import LOCAL_DATABASE as LDB

if TYPE_CHECKING:
    import dataset


async def setup(bot: commands.Bot):
    await bot.add_cog(BaseCog(bot))


class BaseCog(commands.Cog):
    """Base Cog Class"""

    LOCAL_DATABASE = LDB  # TODO I Hate this, need to fix it later

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = self.load_configs()
        self.botspam_channel_id = self.config.get("botspam_channel_id")
        self.user_table: dataset.Table = self.LOCAL_DATABASE["user_data"]

    def load_configs(self) -> dict[str, Any]:
        base_config_path = pathlib.Path("./configs/base.yaml").absolute()
        with open(base_config_path) as base_config:
            config = yaml.load(base_config)
        if self.__class__.__name__ == "BaseCog":
            return config
        subclass_config_path = pathlib.Path(f"./configs/{self.__class__.__name__.lower()}.yaml")
        with open(subclass_config_path) as subclass_config:
            config.update(yaml.load(subclass_config))
            return config

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog is Ready!")

    async def _base_error(self, ctx: commands.Context, error):
        print(error)
        message = "Oopsie whoopsie! Something broke :("
        if isinstance(error, commands.CommandOnCooldown):
            message = f"You absolute dingus, you have {round(error.retry_after, 2)} seconds left on your cooldown."
            await ctx.send(message, ephemeral=True, delete_after=20)
        elif isinstance(error, TimeOutException):
            seconds_left = self.increase_timeout(ctx.author.id)
            try:
                if float(seconds_left) <= 120:
                    message = f"Using commands while in timeout has earned you 60 more seconds on your timeout {ctx.author.mention} - you have {seconds_left} seconds left. Additional messages will not be acknowledged until the timeout is over."
                    await ctx.send(message)
            except Exception as e:
                print(e)
            return
        else:
            await ctx.send(message, delete_after=5.0)

    def increase_timeout(self, user_id: int):
        user_table: dataset.Table = self.LOCAL_DATABASE["user_data"]
        user = user_table.find_one(user_id=user_id)
        if user:
            timeout_until = user.get("timeout_until", 0)
        if timeout_until:
            new_timeout = timeout_until + timedelta(seconds=60)
            user_table.update(dict(user_id=user_id, timeout_until=new_timeout), ["user_id"])
            return (new_timeout - datetime.now()).seconds


def author_in_timeout(user_id: int) -> bool:
    user_table: dataset.Table = BaseCog.LOCAL_DATABASE["user_data"]
    user = user_table.find_one(user_id=user_id)
    if not user:
        return False
    timeout_until = user.get("timeout_until", 0)
    if not timeout_until:
        return False
    if datetime.now() > timeout_until:
        return False
    return True


def punish_timeouts():
    async def check_timeout(ctx: commands.Context):
        if author_in_timeout(ctx.author.id):
            raise TimeOutException("User is in timeout!")
        return True

    return commands.check(check_timeout)
