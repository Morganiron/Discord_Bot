from random import choice, randint
from typing import Optional

from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Member


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    # can add name=" ", aliases=["",""], hidden=True/False
    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'What up?'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll"])
    async def roll_dice(self, ctx, die_string: Optional[str] = "1d6"):
        dice, value = (int(term) for term in die_string.split("d"))
        rolls = [randint(1, value) for i in range(dice)]

        await ctx.send(f"{sum(rolls)}")

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.display_name} for {reason}!")

    @command(name="echo", aliases=["say"])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
    # bot.scheduler.add_job(..)
