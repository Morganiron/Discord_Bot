from asyncio import sleep
from datetime import datetime
from glob import glob
from pathlib import Path
from ..db import db

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands.errors import CommandNotFound


PREFIX = "+"
OWNER_IDS = [523452190942298113]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS)

    def setup(self):

        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")

        print("setup complete")

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        path = Path(__file__).parent / "token.0"
        self.TOKEN = path.read_text()
        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

    async def rules_reminder(self):
        await self.stdout.send("Remember to follow the rules!")

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        await self.stdout.send("An error ocurred")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:

            self.guild = self.get_guild(524332763898445827)
            self.stdout = self.get_channel(604570724199301131)
            self.scheduler.add_job(
                self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()

            # embed = Embed(title="Now online!", description="The bot is now online.",
            #               color=0xFF0000, timestamp=datetime.utcnow())
            # fields = [("Header", "Content", True),
            #           ("Header to the right", "Content", True),
            #           ("A non-inline field", "This field will appear on it's own row", False)]
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)
            # embed.set_footer(text="Footer appears here")
            # embed.set_author(name="Author Name", icon_url=self.guild.icon_url)##icon url optional <- currently set to show the server icon
            # embed.set_thumbnail(url=self.guild.icon_url)
            # embed.set_image(url=self.guild.icon_url)
            # await channel.send(embed=embed)

            # await channel.send(file=File("./data/images/channelBanner.jpg"))

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("bot ready")
            await self.stdout.send("Now Online!")

        else:
            print("bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
