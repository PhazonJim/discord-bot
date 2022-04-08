import random
import os
from datetime import timedelta
from discord.ext import commands
from db import db

USER_TABLE = os.environ.get("USER_TABLE")


class Bingus(commands.Cog):
    """All Bingus commands"""

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(
        name="bingusbox",
        brief="Take a spin and see what comes out the other end",
        help="Use this command to earn pain",
    )
    async def _bingusbox(self, ctx):
        res = random.choices(
            population=["slowmodeon", "slowmodeoff", "timeout", "nothing", "black"],
            weights=[0.04, 0.04, 0.20, 0.70, 0.02],
            k=1,
        )[0]
        if res == "slowmodeon":
            await handle_slowmode_more(ctx)
        if res == "slowmodeoff":
            await handle_slowmode_less(ctx)
        if res == "timeout":
            await handle_timeout(ctx)
        if res == "nothing":
            await handle_nothing(ctx)
        if res == "black":
            role_id = int(os.environ.get("SECRET_ROLE_ID"))
            role = ctx.guild.get_role(role_id)
            await handle_black_role(ctx, role)
        return

    @_bingusbox.error
    async def _bingusbox_error(self, ctx, error):
        print(error)
        message = "Foo"
        if isinstance(error, commands.CommandOnCooldown):
            message = f"You absolute dingus, you have {round(error.retry_after, 2)} seconds left on your cooldown."
        await ctx.send(message, delete_after=5)


def add_medal(user_id):
    table = db[USER_TABLE]
    user = table.find_one(user_id=user_id)
    if not user:
        db[USER_TABLE].insert(dict(user_id=user_id, medal_count=1))
        return 1
    medal_count = user.get("medal_count", 0)
    medal_count = medal_count + 1 if medal_count else 1
    db[USER_TABLE].update(dict(user_id=user_id, medal_count=medal_count), ["user_id"])
    return medal_count


def add_punishment(user_id):
    table = db[USER_TABLE]
    user = table.find_one(user_id=user_id)
    if not user:
        db[USER_TABLE].insert(dict(user_id=user_id, punishment_count=1))
        return 1
    punishment_count = user.get("punishment_count", 0)
    punishment_count = punishment_count + 1 if punishment_count else 1
    db[USER_TABLE].update(
        dict(user_id=user_id, punishment_count=punishment_count), ["user_id"]
    )
    return punishment_count


async def handle_slowmode_more(ctx):
    chet_channel_id = int(os.environ.get("CHET_CHANNEL_ID"))
    chet_channel = ctx.guild.get_channel(chet_channel_id)
    delay = chet_channel.slowmode_delay + 15
    await chet_channel.edit(slowmode_delay=delay)
    await chet_channel.send(
        f"Oh frick, {ctx.author.nickname} increased the delay on slowmode."
    )
    await ctx.send(
        f"Oh boy, {ctx.author.mention} updated slowmode in chet to {delay} seconds, thank you!"
    )


async def handle_slowmode_less(ctx):
    chet_channel_id = int(os.environ.get("CHET_CHANNEL_ID"))
    chet_channel = ctx.guild.get_channel(chet_channel_id)
    if chet_channel.slowmode_delay > 0:
        delay = chet_channel.slowmode_delay - 15
        if delay < 0:
            delay = 0
        await chet_channel.edit(slowmode_delay=delay)
        await ctx.send(
            f"{ctx.author.mention}, you have updated the slowmode in chet to {delay} seconds, guess we aren't having fun then."
        )
    else:
        await ctx.send(
            f"{ctx.author.mention}, you rolled for a slowmode decrease but its already dead! Try again."
        )


async def handle_timeout(ctx):
    timeout = timedelta(seconds=60)
    try:
        await ctx.author.timeout_for(timeout)
        await ctx.send(
            f"Oopsie whoopsie {ctx.author.mention} has been put in timeout!! Thats the cost of gambling."
        )
    except:
        total_punishments = add_punishment(ctx.author.id)
        await ctx.send(
            f"{ctx.author.mention} has won a timeout! But I wasn't able to put them in one. Instead they earned a :poop:\nLook at their nasty collection: {total_punishments*':poop:'}"
        )


async def handle_nothing(ctx):
    total_medals = add_medal(ctx.author.id)
    gold, rem = divmod(total_medals, 100)
    silver, bronze = divmod(rem, 10)
    medals = (
        gold * ":first_place:" + silver * ":second_place:" + bronze * ":third_place:"
    )
    await ctx.message.channel.send(
        f"{ctx.author.mention}, you didn't win anything, but here is a nice medal for trying: :third_place:\nHere is your collection: {medals}"
    )


async def handle_black_role(ctx, role):
    if ctx.author not in role.members:
        for member in role.members:
            await member.remove_roles(role)
            await ctx.send(
                f"{ctx.author.mention} has stolen the highly cherished black role from {member.mention}!"
            )
        await ctx.author.add_roles(role)
    else:
        await ctx.send(
            f"{ctx.author.mention}, you have been stripped of the black role. Better get rollin."
        )
        await ctx.author.remove_roles(role)
