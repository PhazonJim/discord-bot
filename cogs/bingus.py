import os
import random
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from discord.ext import commands

from db import LOCAL_DATABASE

if TYPE_CHECKING:
    import dataset


async def setup(bot: commands.Bot):
    await bot.add_cog(Bingus(bot))


class TimeOutException(commands.CommandError):
    pass


class Bingus(commands.Cog):
    """All Bingus commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.table: dataset.Table = LOCAL_DATABASE["user_data"]
        self.chet_channel_id = int(os.environ.get("CHET_CHANNEL_ID"))
        self.secret_role_id = int(os.environ.get("SECRET_ROLE_ID"))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bingus is Ready!")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(
        name="bingusbox",
        brief="Take a spin and see what comes out the other end",
        help="Use this command to earn pain",
    )
    async def _bingusbox(self, ctx: commands.Context):
        if self.author_in_timeout(ctx.author.id):
            raise TimeOutException("User is lite-muted.")
        # weights=[0.00, 1.00, 0.00, 0.00, 0.00]
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
        print(error)
        message = "Oopsie whoopsie! Something broke :("
        if isinstance(error, commands.CommandOnCooldown):
            message = f"You absolute dingus, you have {round(error.retry_after, 2)} seconds left on your cooldown."
            await ctx.send(message)
        elif isinstance(error, TimeOutException):
            message = f"Nice try but you're muted {ctx.author.mention}"
            await ctx.send(message)
        else:
            await ctx.send(message, delete_after=5.0)

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
        if ctx.author not in role.members:
            for member in role.members:
                await member.remove_roles(role)
                await ctx.send(f"{ctx.author.mention} has stolen the highly cherished black role from {member.display_name}!")
            await ctx.author.add_roles(role)
        else:
            await ctx.send(f"{ctx.author.mention}, you have been stripped of the black role. Better get rollin.")
            await ctx.author.remove_roles(role)

    def add_punishment(self, user_id: int) -> int:
        user = self.table.find_one(user_id=user_id)
        if not user:
            self.table.insert(dict(user_id=user_id, punishment_count=1))
            return 1
        punishment_count = user.get("punishment_count", 0)
        punishment_count = punishment_count + 1 if punishment_count else 1
        self.table.update(dict(user_id=user_id, punishment_count=punishment_count), ["user_id"])
        return punishment_count

    def add_timeout(self, user_id: int):
        timeout_until = datetime.now() + timedelta(seconds=60)
        user = self.table.find_one(user_id=user_id)
        if not user:
            self.table.insert(dict(user_id=user_id, timeout_until=timeout_until))
            return
        self.table.update(dict(user_id=user_id, timeout_until=timeout_until), ["user_id"])

    def author_in_timeout(self, user_id: int) -> bool:
        user = self.table.find_one(user_id=user_id)
        if not user:
            return False
        timeout_until = user.get("timeout_until", 0)
        if not timeout_until:
            return False
        if datetime.now() > timeout_until:
            return False
        return True

    def add_medal(self, user_id: int) -> int:
        user = self.table.find_one(user_id=user_id)
        if not user:
            self.table.insert(dict(user_id=user_id, medal_count=1))
            return 1
        medal_count = user.get("medal_count", 0)
        medal_count = medal_count + 1 if medal_count else 1
        self.table.update(dict(user_id=user_id, medal_count=medal_count), ["user_id"])
        return medal_count

    # async def handle_slowmode_more(self, ctx: commands.Context):
    #     chet_channel = await ctx.guild.fetch_channel(self.chet_channel_id)
    #     delay = chet_channel.slowmode_delay + 15
    #     await chet_channel.edit(slowmode_delay=delay)
    #     await chet_channel.send(f"Oh frick, {ctx.author.display_name} increased the delay on slowmode.")
    #     await ctx.send(f"Oh boy, {ctx.author.display_name} updated slowmode in chet to {delay} seconds, thank you!")

    # async def handle_slowmode_less(self, ctx: commands.Context):
    #     chet_channel = await ctx.guild.fetch_channel(self.chet_channel_id)
    #     if chet_channel.slowmode_delay > 0:
    #         delay = chet_channel.slowmode_delay - 15
    #         if delay < 0:
    #             delay = 0
    #         await chet_channel.edit(slowmode_delay=delay)
    #         await ctx.send(f"{ctx.author.mention}, you have updated the slowmode in chet to {delay} seconds, guess we aren't having fun then.")
    #     else:
    #         await ctx.send(f"{ctx.author.mention}, you rolled for a slowmode decrease but its already dead! Try again.")
