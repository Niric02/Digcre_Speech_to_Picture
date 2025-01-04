import logging
import os

import discord
import discord.ext.commands as commands
import replicate
from dotenv import load_dotenv

import discordbot.Discord as discbot
from speech_recogniser.ReplicateTranscriber import ReplicateTranscriber
from speech_to_picture.ImageFromSpeech import ImageFromSpeech

if __name__ == "__main__":
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    AZUREKEY = os.getenv('AZURE_KEY')
    REGION = os.getenv('REGION')
    REPLICATEKEY = os.getenv('REPLICATE_API_TOKEN')
    LANGUAGE = os.getenv('LANGUAGE', default="auto")
    RECORDING_LENGTH = int(os.getenv('RECORDING_LENGTH', default="0"))

    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "./logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Construct the full path to save the image
    log_file = os.path.join(logs_dir, "bot_logs.log")

    logging.basicConfig(
        format="{asctime} - {name} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,  # Set the logging level
    )

    # Create a file handler to write logs to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)  # Set the file logging level

    # Create a logger and add both handlers
    logger = logging.getLogger('bot')
    logger.setLevel(logging.INFO)  # Set the overall logging level
    logger.addHandler(file_handler)

    # Log initialization messages
    logger.info("Initializing the bot...")

    replicate_client = replicate.Client(REPLICATEKEY)
    intents = discord.Intents.all()

    imager = ImageFromSpeech(replicate_client, logger)

    bot = commands.Bot(command_prefix='!', intents=intents)
    transcriber = ReplicateTranscriber(replicate_client, logger, LANGUAGE)

    bot.add_cog(
        discbot.DiscordBot(bot, transcriber, imager.generate_image_from_transcription, logger, RECORDING_LENGTH))

    bot.run(TOKEN)
