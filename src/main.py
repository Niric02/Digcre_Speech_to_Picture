import os
from dotenv import load_dotenv
import discord
import discord.ext.commands as commands
import discordbot.Discord as discbot
from speech_recogniser.ReplicateTranscriber import ReplicateTranscriber

if __name__ == "__main__":
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    AZUREKEY = os.getenv('AZURE_KEY')
    REGION = os.getenv('REGION')
    REPLICATEKEY = os.getenv('REPLICATE_API_TOKEN')


    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='/', intents=intents)
    transcriber = ReplicateTranscriber(REPLICATEKEY)

    bot.add_cog(discbot.DiscordBot(bot,transcriber))

    bot.run(TOKEN)



