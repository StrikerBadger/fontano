# This file contains the commands that I need for ETH place

import nextcord
from nextcord.ext import commands
from PIL import Image
import bot_values


class Place(commands.Cog):
    def __init__(self, bot):
        self.transparency_bound = 204 # 80% (Alpha value)
        self.draw_channel = 819966095070330950 #eth-place-bots
        self.bot = bot

    # Draw a picture onto ETH-Place
    @commands.command(description="Starts the drawing process for a given picture (Developer only)")
    async def draw(self, ctx, filepath, xpos, ypos):
        # Check if message author is me
        if ctx.author.id not in bot_values.aaron_ids:
            await ctx.send("This command is reserved for the bot's developer.")
            return
        # Load image, set channel and start placing pixels
        # Set channel here
        image = Image.open(filepath).convert("RGBA")
        width = image.width
        height = image.height
        burst_count = 1
        for i in range(width):
            for j in range(height):
                x, y = int(xpos)+j, int(ypos)+i
                pixel = image.getpixel((x, y))
                # Check for transperancy bound
                if pixel[3] < self.transparency_bound:
                    continue
                await ctx.send(f".place setpixel {x} {y} {self.rgb_to_hex((pixel[:3]))}")
        image.close()

    # To convert rgb values to hex color values
    def rgb_to_hex(self, rgb):
        r = f"0x0{hex(rgb[0])}" if rgb[0] < 16 else str(hex(rgb[0]))
        g = f"0x0{hex(rgb[1])}" if rgb[1] < 16 else str(hex(rgb[1]))
        b = f"0x0{hex(rgb[2])}" if rgb[2] < 16 else str(hex(rgb[2]))
        return f"#{r[-2:]}{g[-2:]}{b[-2:]}"