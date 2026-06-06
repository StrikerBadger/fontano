from os import environ
import discord
from discord.ext import commands

DEBUG = True
ADMINS = [481917645067780097]
in_relaymode = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='fon ', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def relaystart(ctx, channel_id=768600365602963496): # By default this is the ETH-DINFK #spam channel
    if ctx.author.id not in ADMINS or ctx.author.id in in_relaymode:
        await ctx.send('You cannot use Relay-Mode or you may already have relays active!')
        return
    in_relaymode[ctx.author.id] = int(channel_id)
    await ctx.send(f'Relay-Mode activated for channel <#{channel_id}>.')

@bot.command()
async def relay(ctx, message):
    if ctx.author.id not in in_relaymode:
        await ctx.send('You are not currently in Relay-Mode.')
        return
    relay_channel = await bot.fetch_channel(in_relaymode[ctx.author.id])
    if DEBUG:
        print(f'Channel is {relay_channel.id}')
    await relay_channel.send(message)

@bot.command()
async def relaystop(ctx):
    if ctx.author.id in in_relaymode:
        in_relaymode.pop(ctx.author.id)
    await ctx.send('Relay-Mode is off now.')

@bot.event
async def on_message(message):
    if bot.user.id == message.author.id:
        return
    if message.channel.id in in_relaymode.values():
        for relayee_id, relaychannel_id in in_relaymode.items():
            if relaychannel_id in in_relaymode.values():
                dm = await bot.create_dm(bot.get_user(relayee_id))
                await dm.send(
                    f'Channel: <#{relaychannel_id}> From: <@{message.author.id}>\n' + \
                    message.content
                )
    await bot.process_commands(message)


bot.run(environ.get('FONTANO_TOKEN'))
