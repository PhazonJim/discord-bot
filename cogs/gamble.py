import os
import random
from datetime import datetime, timedelta

from discord.ext import commands

from cogs.base import Bingus, punish_timeouts


async def setup(bot: commands.Bot):
    await bot.add_cog(Gamble(bot))


class Gamble(Bingus):
    """All Bingus commands"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot=bot)
        self.chet_channel_id = int(os.environ.get("CHET_CHANNEL_ID"))
        self.secret_role_id = int(os.environ.get("SECRET_ROLE_ID"))

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(
        name="bingusbox",
        brief="Take a spin and see what comes out the other end",
        help="Use this command to earn pain",
    )
    @punish_timeouts()
    async def _bingusbox(self, ctx: commands.Context):
        if ctx.channel.id != self.botspam_channel_id:
            return
        weights = [0.04, 0.04, 0.20, 0.70, 0.02]
        res = random.choices(
            population=["slowmodeon", "slowmodeoff", "timeout", "nothing", "black"],
            weights=weights,
            k=1,
        )[0]
        if res == "slowmodeon":
            await self.handle_nothing(ctx)
        if res == "slowmodeoff":
            await self.handle_nothing(ctx)
        if res == "timeout":
            await self.handle_timeout(ctx)
        if res == "nothing":
            await self.handle_nothing(ctx)
        if res == "black":
            await self.handle_black_role(ctx)
        return

    @_bingusbox.error
    async def _bingusbox_error(self, ctx: commands.Context, error):
        await self._bingus_error(ctx=ctx, error=error)

    async def handle_timeout(self, ctx: commands.Context):
        try:
            self.add_timeout(ctx.author.id)
            await ctx.send(f"Oopsie whoopsie {ctx.author.mention} has been put in timeout!! Thats the cost of gambling.")
        except Exception as e:
            print(e)
            total_punishments = self.add_punishment(ctx.author.id)
            await ctx.send(
                f"{ctx.author.mention} has won a timeout! But I wasn't able to put them in one. Instead they earned a :poop:\nLook at their nasty collection: {total_punishments*':poop:'}"
            )

    async def handle_nothing(self, ctx: commands.Context):
        total_medals = self.add_medal(user_id=ctx.author.id)
        gold, rem = divmod(total_medals, 100)
        silver, bronze = divmod(rem, 10)
        medals = gold * ":first_place:" + silver * ":second_place:" + bronze * ":third_place:"
        await ctx.message.channel.send(
            f"{ctx.author.mention}, you didn't win anything, but here is a nice medal for trying: :third_place:\nHere is your collection: {medals}"
        )

    async def handle_black_role(self, ctx: commands.Context):
        role = ctx.guild.get_role(self.secret_role_id)
        print(role)
        if ctx.author not in role.members:
            for member in role.members:
                await member.remove_roles(role)
                await ctx.send(f"{ctx.author.mention} has stolen the highly cherished Blahaj Blast role from {member.display_name}!")
            await ctx.author.add_roles(role)
        else:
            await ctx.send(f"{ctx.author.mention}, you have been stripped of the Blahaj Blast. Better get rollin.")
            await ctx.author.remove_roles(role)

    def add_punishment(self, user_id: int) -> int:
        user = self.user_table.find_one(user_id=user_id)
        if not user:
            self.user_table.insert(dict(user_id=user_id, punishment_count=1))
            return 1
        punishment_count = user.get("punishment_count", 0)
        punishment_count = punishment_count + 1 if punishment_count else 1
        self.user_table.update(dict(user_id=user_id, punishment_count=punishment_count), ["user_id"])
        return punishment_count

    def add_timeout(self, user_id: int):
        timeout_until = datetime.now() + timedelta(seconds=60)
        user = self.user_table.find_one(user_id=user_id)
        if not user:
            self.user_table.insert(dict(user_id=user_id, timeout_until=timeout_until))
            return
        self.user_table.update(dict(user_id=user_id, timeout_until=timeout_until), ["user_id"])

    def add_medal(self, user_id: int) -> int:
        user = self.user_table.find_one(user_id=user_id)
        if not user:
            self.user_table.insert(dict(user_id=user_id, medal_count=1))
            return 1
        medal_count = user.get("medal_count", 0)
        medal_count = medal_count + 1 if medal_count else 1
        self.user_table.update(dict(user_id=user_id, medal_count=medal_count), ["user_id"])
        return medal_count
