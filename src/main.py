import os
from dotenv import load_dotenv
import discord
import discord.ext.commands as commands
import discordbot.Discord as discbot

if __name__ == "__main__":
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    bot.add_cog(discbot.DiscordBot(bot))

    bot.run(TOKEN)



