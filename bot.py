from os import environ
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='fon ', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(environ.get('FONTANO_TOKEN'))
