from nextcord.ext import commands
from cogs.basic import Basic
from cogs.place import Place
import bot_values
import db_interface

bot_token = ""

bot = commands.Bot(command_prefix=r"fon ")
bot.remove_command("help")

db_interface.createtables(bot_values.tables)

bot.add_cog(Basic(bot))
bot.add_cog(Place(bot))

bot.run(bot_token)