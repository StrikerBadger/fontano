import nextcord
import bot_values

client = nextcord.Client()
bot = nextcord.ext.Bot(command_prefix='$')

@client.event
async def on_ready():
    print(f"{client.user} is now online!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(bot_values.bot_token)