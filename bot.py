from os import environ
from sys import argv
import discord
from discord.ext import tasks, commands
import datetime as dt
import aiohttp
from matplotlib import pyplot as plt
from matplotlib import colors, cm

DEBUG = len(argv) > 1 and argv[1].lower() == 'debug'
BOT_TOKEN = environ.get('FONDEVO_TOKEN') if DEBUG\
            else environ.get('FONTANO_TOKEN')
ADMINS = [481917645067780097, 420702343860977695]

WEATHER_URL = r'https://api.open-meteo.com/v1/forecast?latitude=47.376412&longitude=8.547674&daily=sunrise,sunset&hourly=temperature_2m,apparent_temperature,precipitation_probability,precipitation,wind_speed_10m,uv_index&timezone=Europe%2FBerlin&forecast_days=1'

if DEBUG:
    print('Bot starts in Debug-Mode.')
else:
    print('Bot starts in Normal-Mode.')

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
async def relay(ctx, *, message):
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

async def send_briefing(ctx=None):

    if ctx is not None:
        await ctx.send('Your first briefing.')
    else:
        #TODO: Send to each subscriber if called per task
        pass

@bot.command(name='briefing')
async def briefing_command(ctx):
    if DEBUG:
        await briefing_task()
    await send_briefing(ctx=ctx)

# This will GET weather data, create graphs and then send it out to subscribers
@tasks.loop(time=dt.time(hour=6))
async def briefing_task():
    # Get the weather data
    weather_json = None
    async with aiohttp.ClientSession() as http_client_session:
        async with http_client_session.get(WEATHER_URL) as response:
            weather_json = await response.json()
    # Label figures and axis
    fig, axs = plt.subplots(2, 2)
    fig.suptitle(f"ETH Zentrum Weather {weather_json['daily']['time']}")
    axs[0, 0].set_title('Temperature (2m)')
    axs[0, 0].set_ylabel(weather_json['hourly_units']['temperature_2m'])
    axs[0, 0].set_xlabel('Hour of the Day')
    axs[0, 1].set_title('Precipitation')
    axs[0, 1].set_ylabel(weather_json['hourly_units']['precipitation_probability'])
    axs[0, 1].set_xlabel('Hour of the Day')
    axs[1, 0].set_title('UV Index')
    axs[1, 0].set_ylabel('UV Index')
    axs[1, 0].set_xlabel('Hour of the Day')
    axs[1, 1].set_title('Wind (10M)')
    axs[1, 1].set_ylabel(weather_json['hourly_units']['wind_speed_10m'])
    axs[1, 1].set_xlabel('Hour of the Day')
    # Format the hours once for reuse
    hours = [dt.datetime.fromisoformat(x).hour for x in weather_json['hourly']['time']]
    # Plot the temperature
    axs[0, 0].bar(hours, weather_json['hourly']['temperature_2m'], label='Air Temperature')
    axs[0, 0].plot(hours, weather_json['hourly']['apparent_temperature'], label='Apparent Temperature')
    axs[0, 0].legend()
    # Plot the precipitation
    cmap = plt.get_cmap('Greys')
    norm = colors.Normalize(vmin=min(weather_json['hourly']['precipitation']), vmax=max(weather_json['hourly']['precipitation']))
    bar_colors = [cmap(norm(value)) for value in weather_json['hourly']['precipitation']]
    axs[0, 1].bar(hours, weather_json['hourly']['precipitation_probability'], color=bar_colors, label='Precipitation Probability')
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Dummy array needed for matplotlib
    cbar = fig.colorbar(sm, ax=axs[0, 1])
    cbar.set_label(f"Precipitation Amount in {weather_json['hourly']['precipitation']}")
    axs[0, 1].legend()
    # Plot the UV Index
    axs[1, 0].bar(hours, weather_json['hourly']['uv_index'])
    axs[1, 0].set_ylim(12) # Technically could be higher but at a 12 you should not be out in the sun anyway
    # Plot the wind
    axs[1, 1].bar(hours, weather_json['hourly']['wind_speed_10m'])
    fig.savefig('weather.png', format='png')
    plt.close(fig)
    await send_briefing()


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


bot.run(BOT_TOKEN)