import nextcord
from nextcord.ext import commands
import bot_values

bot = commands.Bot(command_prefix='$')

@bot.command()
async def echo(ctx, message):
    await ctx.send(message)

bot.run(bot_values.bot_token)