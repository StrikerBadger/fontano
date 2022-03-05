# This file contains simple, miscellaneous commands that don't belong in any other category

import nextcord
from nextcord.ext import commands
import time
import bot_values

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # The help command
    @commands.command(description="Shows this page")
    async def help(self, ctx):
        """
        This command shows the help page
        """
        # Create embed
        help_embed = nextcord.Embed(color=0xff0000, title=":question: Help Page", description=":bulb: Here is your help that you requested :bulb:")
        # Walk through all commands
        for command in self.walk_commands():
            description = command.description
            if not description or description == None or description == "":
                description = "No Description found"
            help_embed.add_field(name=f"`fon {command.name}`", value=description)
        await ctx.send(embed=help_embed)

    # A ping command that shows NRTT and heartbeat
    @commands.command(description="Shows Latency values")
    async def ping(self, ctx):
        """
        Shows Network Roundtrip Time and the bot latency (heartbeat)
        """
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
    

    # A simple "say"-type command
    @commands.command(description="Echoes any text message given (Developer only)")
    async def echo(self, ctx, message):
        """
        Sends back the message that it has been given
        """
        # If author is not Aaron, don't echo
        if ctx.author.id not in bot_values.aaron_ids:
            await ctx.send("This command is reserved for the bot's developer.")
            return
        await ctx.send(message)

