# This file contains the commands that I need for ETH place

import nextcord
from nextcord.ext import commands
from PIL import Image
import time
import bot_values


class Place(commands.Cog):
    def __init__(self, bot):
        self.transparency_bound = 204 # 80% (Alpha value)
        self.wait_period = 0.5 # 0.5 seconds
        self.draw_channel = 819966095070330950 #eth-place-bots
        self.burst = 5 # How many pixels to send at once
        self.bot = bot

    # Draw a picture onto ETH-Place
    @commands.command(description="Starts the drawing process for a given picture (Developer only)")
    async def draw(self, ctx, filepath, xpos, ypos):
        # Check if message author is me
        if ctx.author.id not in bot_values.aaron_ids:
            await ctx.send("This command is reserved for the bot's developer.")
            return
        # Load image, set channel and start placing pixels
        ctx.channel = self.draw_channel
        image = Image.open(filepath).convert("RGBA")
        width = image.width
        height = image.height
        burst_count = 1
        for i in range(width):
            for j in range(height):
                x, y = xpos+j, ypos+i
                pixel = image.getpixel((x, y))
                # Check for transperancy bound
                if pixel[3] < self.transparency_bound:
                    continue
                if burst_count % self.burst == 0:
                    await time.sleep(self.wait_period)
                    burst_count = 0
                await ctx.send(f".place setpixel {x} {y} {self.rgb_to_hex(pixel[:3])}")

    # To convert rgb values to hex color values
    def rgb_to_hex(rgb):
        return f"#{hex(rgb[0])}{hex(rgb[1])}{hex(rgb[2])}"