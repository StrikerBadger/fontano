import nextcord
from nextcord.ext import commands
import cogs
from cogs.basic import Basic
import bot_values

bot = commands.Bot(command_prefix=r"fon ")
bot.remove_command("help")

bot.add_cog(Basic(bot))

bot.run(bot_values.bot_token)