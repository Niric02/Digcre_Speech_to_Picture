import os
import discord
from discord.ext import commands


class DiscordBot(commands.Cog):
    def __init__(self, bot, transcriber):
        self.bot = bot
        self.transcriber = transcriber

    connections = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f'{self.bot.user} is connected to the following guilds: {self.bot.guilds}\n'
        )

    @commands.command(name='join')
    async def join(self, ctx):
        """Command for the bot to join the user's voice channel."""
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            vc = await voice_channel.connect()
            await ctx.send(f"Joined {voice_channel.name}!")
            self.connections[ctx.guild.id] = vc
            vc.start_recording(
                discord.sinks.WaveSink(),  # The sink type to use.
                self.once_done,  # What to do once done.
                ctx.channel  # The channel to disconnect from.
            )
        else:
            await ctx.send("You need to be in a voice channel for me to join!")

    @commands.command(name='leave')
    async def leave(self, ctx):
        """Command for the bot to leave the voice channel."""
        # Check if the bot is connected to a voice channel
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from the voice channel!")
        else:
            await ctx.send("I'm not in a voice channel!")

    @commands.command(name='stop_recording')
    async def stop_recording(self, ctx):
        if ctx.guild.id in self.connections:  # Check if the guild is in the cache.
            vc = self.connections[ctx.guild.id]
            vc.stop_recording()  # Stop recording, and call the callback (once_done).
            self.connections.pop(ctx.guild.id)  # And delete.
        else:
            await ctx.respond("I am currently not recording here.")  # Respond with this if we aren't recording.

    async def once_done(self, sink: discord.sinks, channel: discord.TextChannel,
                        *args):  # Our voice client already passes these in.
        recorded_users = [  # A list of recorded users
            f"<@{user_id}>"
            for user_id, audio in sink.audio_data.items()
        ]
        await sink.vc.disconnect()  # Disconnect from the voice channel.
        files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in
                 sink.audio_data.items()]  # List down the files.
        text = {}
        for user_id, audio in sink.audio_data.items():
            file_path = os.path.join(".", f"{user_id}.wav")  # Save as WAV files

            # Save the audio data to a .wav file
            with open(file_path, "wb") as f:
                f.write(audio.file.getbuffer())  # Write the byte data to the file

            text[user_id] = self.transcriber.from_file(file_path)
            print(text)
        await channel.send(f"finished recording audio for: {', '.join(recorded_users)}. \n "
                           f"the following text was transcribed: {text}")  # Send a message with the accumulated files.
