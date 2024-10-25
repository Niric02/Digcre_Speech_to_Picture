import os
from dotenv import load_dotenv
import discord
import discord.ext.commands as commands
import discordbot.Discord as discbot
from speech_recogniser.azure_transcriber import Transcriber

if __name__ == "__main__":
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    AZUREKEY = os.getenv('AZURE_KEY')
    REGION = os.getenv('REGION')


    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='/', intents=intents)
    transcriber = Transcriber(key = AZUREKEY,region=REGION)

    bot.add_cog(discbot.DiscordBot(bot,transcriber))

    bot.run(TOKEN)



