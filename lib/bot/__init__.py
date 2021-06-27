from datetime import datetime
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord import Embed, File
from discord.ext.commands.errors import CommandNotFound

PREFIX = "+"
OWNER_IDS = [523452190942298113]

class Bot(BotBase):
    def __init__(self):       
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        
        super().__init__(
            command_prefix = PREFIX,
            owner_ids = OWNER_IDS)
        
    def run(self, version):
        self.VERSION = version        
        
        path = Path(__file__).parent / "token.0"
        self.TOKEN = path.read_text()
        print("running bot...")
        super().run(self.TOKEN, reconnect=True)
            
            
    
    async def on_connect(self):
        print("bot connected")
        
    async def on_disconnect(self):
        print("bot disconnected")
        
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")
            
        else:
            channel = self.get_channel(604570724199301131)
            await channel.send("An error ocurred")          
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
            self.ready = True
            self.guild = self.get_guild(524332763898445827)
            print("bot ready")
            
            channel = self.get_channel(604570724199301131)
            await channel.send("Now Online!")
            
            embed = Embed(title="Now online!", description="The bot is now online.", 
                          color=0xFF0000, timestamp=datetime.utcnow())
            fields = [("Header", "Content", True),
                      ("Header to the right", "Content", True),
                      ("A non-inline field", "This field will appear on it's own row", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_footer(text="Footer appears here")
            embed.set_author(name="Author Name", icon_url=self.guild.icon_url)##icon url optional <- currently set to show the server icon
            embed.set_thumbnail(url=self.guild.icon_url)
            embed.set_image(url=self.guild.icon_url)
            await channel.send(embed=embed)
            
            await channel.send(file=File("./data/images/channelBanner.jpg"))
            
        
        else:
            print("bot reconnected")
        
    async def on_message(self, message):
        pass

bot = Bot()