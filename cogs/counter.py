import re

from discord.ext import commands
from sympy import sympify

from cogs.base import Bingus


async def setup(bot: commands.Bot):
    await bot.add_cog(Counter(bot))


class Counter(Bingus):
    """All Bingus commands"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot=bot)
        self.next_number = 1
        self.record_number = 0
        self.record_message = None

    # @punish_timeouts
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(
        name="binguscount",
        brief="Take a spin and see what comes out the other end",
        help="Use this command to earn pain",
    )
    async def _binguscount(self, ctx: commands.Context, *args):
        formula = " ".join(args)
        result = re.sub("[^0-9+-.()*/^ ]", "", formula)
        result = sympify(formula)
        if result == self.next_number:
            if result > self.record_number:
                self.record_number = result
                await ctx.message.add_reaction("🏆")
                if self.record_message:
                    await self.record_message.clear_reaction("🏆")
                self.record_message = ctx.message
            self.next_number += 1
            await ctx.message.add_reaction("✅")
        else:
            self.next_number = 1
            await ctx.message.add_reaction("❌")
            await ctx.message.reply(f"Wow someone is bad at math... Previous record: {self.record_number}", mention_author=False)

    @_binguscount.error
    async def _binguscount_error(self, ctx: commands.Context, error):
        await self._bingus_error(ctx=ctx, error=error)
