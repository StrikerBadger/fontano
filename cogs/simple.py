# This file contains simple, miscellaneous commands that don't belong in any other category

from unicodedata import name
import nextcord
from nextcord.ext import commands
import time

class Simple(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # A ping command that shows NRTT and heartbeat
    @commands.command()
    async def ping(self, ctx):
        # Calculate the ping time
        start = time.perf_counter()
        await ctx.trigger_typing()
        end = time.perf_counter()
        # Create the strings and embed
        dark_yellow = 0xffe600
        ping_embed = nextcord.Embed(color=dark_yellow, title="Pong! :ping_pong:")
        ping_embed.add_field(name="Network RTT", value=f":globe_with_meridians: `{int((end-start)*1000)}`ms")
        ping_embed.add_field(name=f"Bot Latency", value=f":heart: `{int(self.bot.latency*1000)}`ms")
        await ctx.send(embed=ping_embed)