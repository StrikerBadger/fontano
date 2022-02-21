import nextcord
from nextcord.ext import commands
import cogs
from cogs.simple import Simple
import bot_values

bot = commands.Bot(command_prefix='$')

bot.add_cog(Simple(bot))

bot.run(bot_values.bot_token)