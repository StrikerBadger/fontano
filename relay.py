from discord.ext import commands

class RelayLogic(commands.Cog):
    def __init__(self, bot, debug, admins):
        self.bot = bot
        self.debug = debug
        self.admins = admins
        self.in_relaymode = {}

    @commands.command()
    async def relaystart(self, ctx, channel_id=768600365602963496): # By default this is the ETH-DINFK #spam channel
        if ctx.author.id not in self.admins or ctx.author.id in self.in_relaymode:
            await ctx.send('You cannot use Relay-Mode or you may already have relays active!')
            return
        self.in_relaymode[ctx.author.id] = int(channel_id)
        await ctx.send(f'Relay-Mode activated for channel <#{channel_id}>.')

    @commands.command()
    async def relay(self, ctx, *, message):
        if ctx.author.id not in self.in_relaymode:
            await ctx.send('You are not currently in Relay-Mode.')
            return
        relay_channel = await self.bot.fetch_channel(self.in_relaymode[ctx.author.id])
        if self.debug:
            print(f'Channel is {relay_channel.id}')
        await relay_channel.send(message)
    
    @commands.command()
    async def relaystop(self, ctx):
        if ctx.author.id in self.in_relaymode:
            self.in_relaymode.pop(ctx.author.id)
        await ctx.send('Relay-Mode is off now.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.id == message.author.id:
            return
        if message.channel.id in self.in_relaymode.values():
            for relayee_id, relaychannel_id in self.in_relaymode.items():
                if relaychannel_id in self.in_relaymode.values():
                    dm = await self.bot.create_dm(self.bot.get_user(relayee_id))
                    await dm.send(
                        f'Channel: <#{relaychannel_id}> From: <@{message.author.id}>\n' + \
                        message.content
                    )
        await self.bot.process_commands(message)