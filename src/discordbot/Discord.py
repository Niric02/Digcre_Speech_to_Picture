import os
import discord
from discord import VoiceClient, Guild
from discord.ext import commands
from discord.ext.commands import Context

from speech_recogniser.ReplicateTranscriber import ReplicateTranscriber, TimestampedTranscription


class DiscordBot(commands.Cog):
    def __init__(self, bot, transcriber: ReplicateTranscriber, transcription_callback):
        self.bot = bot
        self.transcriber = transcriber
        self.transcription_callback = transcription_callback

    connections: dict[int, VoiceClient] = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} is connected to the following guilds: {self.bot.guilds}')

    @commands.command(name='join')
    async def join(self, ctx):
        """Command for the bot to join the user's voice channel."""
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            vc = await voice_channel.connect()
            self.connections[ctx.guild.id] = vc
        else:
            await ctx.send("You need to be in a voice channel for me to join!")

    @commands.command(name='leave')
    async def leave(self, ctx):
        """Command for the bot to leave the voice channel."""
        # Check if the bot is connected to a voice channel
        if ctx.guild.id in self.connections:
            vc = self.connections[ctx.guild.id]
            if vc.recording:
                vc.stop_recording()
            await vc.disconnect()
            self.connections.pop(ctx.guild.id)
        else:
            await ctx.send("I'm not in a voice channel!")

    @commands.command(name='start_recording')
    async def start_recording(self, ctx: Context):
        if ctx.guild.id not in self.connections:
            await self.join(ctx)

        if ctx.guild.id in self.connections:
            vc = self.connections[ctx.guild.id]
            if vc.recording:
                await ctx.send("I'm already recording.")
            else:
                vc.start_recording(
                    discord.sinks.WaveSink(),
                    self.once_done,
                    ctx.guild
                )
                await ctx.send("Started recording!")
                print("Recording started")

    @commands.command(name='stop_recording')
    async def stop_recording(self, ctx):
        if ctx.guild.id in self.connections:
            vc = self.connections[ctx.guild.id]
            if vc.recording:
                await ctx.send("Stopped recording!")
                vc.stop_recording()
            else:
                await ctx.send("I'm not recording.")
        else:
            await ctx.send("I'm not in a voice channel!")

    async def once_done(self, sink: discord.sinks.WaveSink, guild: Guild, *args):
        print("Recording stopped")
        transcriptions: list[TimestampedTranscription] = []
        for user_id, audio in sink.audio_data.items():
            file_path = os.path.join(".", f"{user_id}.wav")
            with open(file_path, "wb") as f:
                f.write(audio.file.getbuffer())
            transcriptions.extend(self.transcriber.from_file(file_path, user_id))
        self.transcription_callback(self.transcriptions_to_text(transcriptions, guild))

    def transcriptions_to_text(self, transcriptions: list[TimestampedTranscription], guild: Guild):
        transcriptions.sort(key=lambda x: (x.start, x.end))
        user_identifiers = set([transcription.identifier for transcription in transcriptions])
        user_names = {ident: self.get_name(guild, ident) for ident in user_identifiers}
        previous_user = None
        text = ""
        for transcription in transcriptions:
            if transcription.identifier != previous_user:
                text += f"\n{user_names[transcription.identifier]}: "
                previous_user = transcription.identifier
            text += transcription.text
        return text

    def get_name(self, guild: Guild, ident) -> str:
        member = guild.get_member(ident)
        if member.nick is not None:
            return member.nick
        if member.global_name is not None:
            return member.global_name
        return member.name
