# This file contains the commands that I need for ETH place

from nextcord.ext import commands
from PIL import Image
import bot_values
import db_interface


class Place(commands.Cog):
    def __init__(self, bot):
        self.draw_channel = 819966095070330950 #eth-place-bots
        self.bot = bot
    
    @commands.command(description="Loads a picture into the DB (Developer only)")
    async def loadimage(self, ctx, filepath):
        # Check if message author is me
        if ctx.author.id not in bot_values.aaron_ids:
            await ctx.send("This command is reserved for the bot's developer.")
            return
        # Load pixels and start placing pixels
        image = Image.open(filepath).convert("RGBA")
        db_interface.loadpicture(image)
        image.close()
        await ctx.send("Image got loaded into the DB successfully!")

    # Draw the loaded picture onto ETH-Place
    @commands.command(description="Starts the drawing process for a given picture (Developer only)")
    async def draw(self, ctx, xpos, ypos):
        # Check if message author is me
        if ctx.author.id not in bot_values.aaron_ids:
            await ctx.send("This command is reserved for the bot's developer.")
            return
        # Load pixels and start placing pixels
        pixels = db_interface.query("SELECT * FROM pixels WHERE NOT drawn")
        for pixel in pixels:
            await ctx.send(f".place setpixel {pixel[0] + int(xpos)} {pixel[1] + int(ypos)} {pixel[2]}")
            db_interface.updatequery(f"UPDATE pixels SET drawn=TRUE WHERE xpos={pixel[0]} AND ypos={pixel[1]}")
        await ctx.send("Image done drawing!")
