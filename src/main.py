import os
from dotenv import load_dotenv
import discord
import discordbot.Discord as discbot

if __name__ == "__main__":
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.message_content = True

    bot = discbot.DiscordBot(intents)

    bot.run(TOKEN)


