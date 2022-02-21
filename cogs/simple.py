# This file contains simple, miscellaneous commands that don't belong in any other category

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
        ping_text = f":globe_with_meridians: Ping: {int((end - start) * 1000)}ms"
        heartbeat_text = f" :heart: Heartbeat: {int(self.bot.latency * 1000)}ms"
        ping_embed = nextcord.Embed(title="Pong! :ping_pong:", description=f"{ping_text}\n{heartbeat_text}")
        await ctx.send(embed=ping_embed)