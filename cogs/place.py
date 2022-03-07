# This file contains the commands that I need for ETH place

import nextcord
from nextcord.ext import commands
from PIL import Image
import bot_values

class Place(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Draw a picture onto ETH-Place
    @commands.command(description="Starts the drawing process for a given picture (Developer only)")
    async def draw(self, ctx, filepath, xpos, ypos):
        if ctx.author.id not in bot_values.aaron_ids:
            await ctx.send("This command is reserved for the bot's developer.")
            return
        image = Image.open(filepath)
        width = image.width
        height = image.height
        color_vals = image.
        print(str(image.getpixel((0,0))))