import discord

class DiscordBot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)

    async def on_ready(self):

        print(
            f'{self.user} is connected to the following guilds: {self.guilds}\n'
        )

    async def on_message(self,message):
        if message.author == self.user:
            return

        if message.content.lower() == 'hello':
            await message.channel.send('Hello! How can I help you today?')