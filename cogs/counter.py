from __future__ import annotations

import re
from typing import TYPE_CHECKING

from discord.ext import commands
from sympy import sympify

from cogs.base import Bingus
from db import LOCAL_DATABASE

if TYPE_CHECKING:
    import dataset
    from discord import Message


async def setup(bot: commands.Bot):
    await bot.add_cog(Counter(bot))


class Counter(Bingus):
    """All Bingus commands"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot=bot)
        self.counter_table: dataset.Table = LOCAL_DATABASE["counts"]

    # @punish_timeouts
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(
        name="binguscount",
        brief="Take a spin and see what comes out the other end",
        help="Use this command to earn pain",
    )
    async def _binguscount(self, ctx: commands.Context, *args):
        if ctx.channel.id != self.botspam_channel_id:
            return
        formula = " ".join(args)
        result = re.sub("[^0-9+-.()*/^ ]", "", formula)
        result = int(sympify(formula))
        next_number = self.get_next_number(ctx=ctx)
        record_number = self.get_record_number(ctx=ctx)
        if result == next_number:
            if result > record_number:
                self.update_record_number(ctx=ctx, value=result)
                await ctx.message.add_reaction("🏆")
                record_message = await self.get_record_message(ctx=ctx)
                if record_message:
                    await record_message.clear_reaction("🏆")
                self.update_record_message(ctx=ctx)
            self.update_next_number(ctx=ctx, value=next_number + 1)
            await ctx.message.add_reaction("✅")
        else:
            self.update_next_number(ctx=ctx, value=1)
            await ctx.message.add_reaction("❌")
            await ctx.message.reply(f"Wow someone is bad at math... Previous record: {record_number}", mention_author=False)

    @_binguscount.error
    async def _binguscount_error(self, ctx: commands.Context, error):
        await self._bingus_error(ctx=ctx, error=error)

    def get_next_number(self, ctx: commands.Context) -> int:
        guild = self.counter_table.find_one(guild_id=ctx.guild.id)
        if not guild:
            self.counter_table.insert(dict(guild_id=ctx.guild.id, next_number=1, record_number=0, record_message=None))
            return 1
        return guild.get("next_number")

    def update_next_number(self, ctx: commands.Context, value: int):
        self.counter_table.update(dict(guild_id=ctx.guild.id, next_number=value), ["guild_id"])

    def get_record_number(self, ctx: commands.Context) -> int:
        guild = self.counter_table.find_one(guild_id=ctx.guild.id)
        if not guild:
            self.counter_table.insert(dict(guild_id=ctx.guild.id, next_number=1, record_number=0, record_message=None))
            return 0
        return guild.get("record_number")

    def update_record_number(self, ctx: commands.Context, value: int):
        self.counter_table.update(dict(guild_id=ctx.guild.id, record_number=value), ["guild_id"])

    async def get_record_message(self, ctx: commands.Context) -> Message:
        guild = self.counter_table.find_one(guild_id=ctx.guild.id)
        if not guild:
            self.counter_table.insert(dict(guild_id=ctx.guild.id, next_number=1, record_number=0, record_message=None))
            return None
        message_id = guild.get("record_message")
        if not message_id:
            return None
        message = await ctx.fetch_message(message_id)
        return message

    def update_record_message(self, ctx: commands.Context):
        self.counter_table.update(dict(guild_id=ctx.guild.id, record_message=ctx.message.id), ["guild_id"])
