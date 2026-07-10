from os import environ
from sys import argv
import discord
from discord.ext import tasks, commands
import datetime as dt
import aiohttp
from matplotlib import pyplot as plt
from matplotlib import colors, cm

# Import Cogs
from relay import RelayLogic

DEBUG = len(argv) > 1 and argv[1].lower() == 'debug'
BOT_TOKEN = environ.get('FONDEVO_TOKEN') if DEBUG\
            else environ.get('FONTANO_TOKEN')
ADMINS = [481917645067780097, 420702343860977695]

WEATHER_URL = r'https://api.open-meteo.com/v1/forecast?latitude=47.376412&longitude=8.547674&daily=sunrise,sunset&hourly=temperature_2m,apparent_temperature,precipitation_probability,precipitation,wind_speed_10m,uv_index&timezone=Europe%2FBerlin&forecast_days=1'

if DEBUG:
    print('Bot starts in Debug-Mode.')
else:
    print('Bot starts in Normal-Mode.')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='fon ', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

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
    fig, axs = plt.subplots(2, 2, figsize=(1200, 1200, 'px'), gridspec_kw={'wspace':0.25})
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
    axs[0, 0].plot(hours, weather_json['hourly']['temperature_2m'], label='Air Temperature', c='red')
    axs[0, 0].plot(hours, weather_json['hourly']['apparent_temperature'], label='Apparent Temperature')
    axs[0, 0].grid(which='both')
    axs[0, 0].legend()
    # Plot the precipitation
    cmap = plt.get_cmap('Greys')
    norm = colors.Normalize(vmin=0.0, vmax=max(5.0, max(weather_json['hourly']['precipitation'])))
    bar_colors = [cmap(norm(value)) for value in weather_json['hourly']['precipitation']]
    axs[0, 1].bar(hours, weather_json['hourly']['precipitation_probability'], color=bar_colors, label='Precipitation Probability')
    axs[0, 1].set_ylim(bottom=0.0, top=100.0)
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Dummy array needed for matplotlib
    cbar = fig.colorbar(sm, ax=axs[0, 1])
    cbar.set_label(f"Precipitation Amount in {weather_json['hourly_units']['precipitation']}")
    # Plot the UV Index
    axs[1, 0].bar(hours, weather_json['hourly']['uv_index'], color='orange')
    if DEBUG:
        print(weather_json['hourly']['uv_index'])
    axs[1, 0].set_ylim(bottom=0.0, top=12.0) # Technically could be higher but at a 12 you should not be out in the sun anyway
    # Plot the wind
    axs[1, 1].plot(hours, weather_json['hourly']['wind_speed_10m'])
    axs[1, 1].grid(which='both')
    fig.savefig('weather.png', format='png')
    plt.close(fig)
    await send_briefing()

@bot.event
async def on_ready():
    await bot.add_cog(RelayLogic(bot, debug=DEBUG, admins=ADMINS))

bot.run(BOT_TOKEN)