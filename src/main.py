import os
from dotenv import load_dotenv
import discord
import discord.ext.commands as commands
import discordbot.Discord as discbot
from speech_recogniser.ReplicateTranscriber import ReplicateTranscriber


def example_callback(transcription: str):
    print(transcription)


if __name__ == "__main__":
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    AZUREKEY = os.getenv('AZURE_KEY')
    REGION = os.getenv('REGION')
    REPLICATEKEY = os.getenv('REPLICATE_API_TOKEN')
    LANGUAGE = os.getenv('LANGUAGE', default="auto")
    RECORDING_LENGTH = int(os.getenv('RECORDING_LENGTH', default="0"))

    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix='!', intents=intents)
    transcriber = ReplicateTranscriber(REPLICATEKEY, LANGUAGE)

    bot.add_cog(discbot.DiscordBot(bot, transcriber, example_callback, RECORDING_LENGTH))

    bot.run(TOKEN)
