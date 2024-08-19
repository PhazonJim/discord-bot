import os
import random
from datetime import datetime, timedelta

from discord.ext import commands

from cogs.base import Bingus


async def setup(bot: commands.Bot):
    await bot.add_cog(Lootbox(bot))


class Lootbox(Bingus):
    """All Lootbox Commands"""
    def __init__(self, bot: commands.Bot):
        super().__init__(bot=bot)
        self.chet_channel_id = int(os.environ.get("CHET_CHANNEL_ID"))
        self.secret_role_id = int(os.environ.get("SECRET_ROLE_ID"))
        self.ciggy_role_id = 123456789
        self.vibrate_green_id = 123456789
        # etc, can eventually move them to a dashboard/config file or something easier to access/edit. 


    # LOOTBOX COMMAND / ERROR HANDLING
    @commands.cooldown(1, 360, commands.BucketType.user) # 1 = number of times command can be used before cooldown is triggered, 10= number of seconds the cooldown is 
    @commands.command(
        name="lootbox",
        brief="Take a spin and see what comes out the other end",
        help="Get a lootbox",
    )
    async def _lootbox(self, ctx: commands.Context):
        if ctx.channel.id != self.botspam_channel_id: # not in botspam, ignore and return immediately.
            return
        # TODO: Add lootbox command logic here
        await ctx.message.reply("This command is a WIP")

    @_lootbox.error # In case of an error (such as cooldowns), we are going to fallback to Bingus' error handling
    async def _bingusbox_error(self, ctx: commands.Context, error):
        await self._bingus_error(ctx=ctx, error=error)



    @commands.command(
        name="colourbank",
        brief="You must use this command with either `help`, `check`, `swap`, `clear`, or `spy`",
        help="colourbank help",
    )
    async def _colourbank(self, ctx: commands.Context, *args): #args is anything that is typed after the command
        if ctx.channel.id != self.botspam_channel_id: # not in botspam, ignore and return immediately.
            return
        bad_args_message = "You must use this command with either `help`, `check`, `swap`, `clear`, or `spy`"
        if len(args) != 1:
            await ctx.message.reply(bad_args_message, mention_author=False)
            return
        option = args[0]
        if option not in ["help", "check", "swap", "clear", "spy"]:
            await ctx.message.reply(bad_args_message, mention_author=False)
            return
        else:
            if option == "help":
                # TODO : Handle help
                pass
            if option == "check":
                # TODO: Handle check
                pass
            if option == "swap":
                #TODO: Handle swap
                pass
            if option == "clear":
                #TODO: Handle clear
                pass
            if option == "spy":
                #TODO: Handle spy
                pass
        await ctx.message.reply("This command is a work in progress.")

    @_colourbank.error # In case of an error (such as cooldowns), we are going to fallback to Bingus' error handling
    async def _bingusbox_error(self, ctx: commands.Context, error):
        await self._bingus_error(ctx=ctx, error=error)

