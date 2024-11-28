import os
from asyncio import gather

import discord
from discord import VoiceClient, Guild
from discord.ext import commands
from discord.ext.commands import Context

from speech_recogniser.ReplicateTranscriber import ReplicateTranscriber, TimestampedTranscription


class DiscordBot(commands.Cog):
    def __init__(self, bot, transcriber: ReplicateTranscriber, transcription_callback,logger, recording_length: int):
        self.bot = bot
        self.logger = logger
        self.transcriber = transcriber
        self.transcription_callback = transcription_callback
        self.recording_length = recording_length

    connections: dict[int, VoiceClient] = {}
    recording_in = set()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{self.bot.user} is connected to the following guilds: {self.bot.guilds}')

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
            if ctx.guild.id in self.recording_in:
                await self.stop_recording(ctx)
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
                    discord.sinks.WaveSink(filters={"time": self.recording_length}),
                    self.once_done,
                    ctx
                )
                if ctx.guild.id not in self.recording_in:
                    self.logger.info("Recording started")
                    self.recording_in.add(ctx.guild.id)
                    await ctx.send("Started recording!")

    @commands.command(name='stop_recording')
    async def stop_recording(self, ctx):
        if ctx.guild.id in self.connections:
            vc = self.connections[ctx.guild.id]
            if ctx.guild.id in self.recording_in:
                self.recording_in.remove(ctx.guild.id)
                vc.stop_recording()
                await ctx.send("Stopped recording!")
            else:
                await ctx.send("I'm not recording.")
        else:
            await ctx.send("I'm not in a voice channel!")

    async def once_done(self, sink: discord.sinks.WaveSink, ctx: Context, *args):
        if ctx.guild.id in self.recording_in:
            self.logger.info("Processing recording")
            await self.start_recording(ctx)
        else:
            self.logger.info("Recording stopped")
        transcription_coroutines = []
        for user_id, audio in sink.audio_data.items():
            file_path = os.path.join(".", f"{user_id}.wav")
            with open(file_path, "wb") as f:
                f.write(audio.file.getbuffer())
            transcription_coroutines.append(self.transcriber.from_file(file_path, user_id))
        results = await gather(*transcription_coroutines)
        transcriptions = []
        for result in results:
            transcriptions.extend(result)
        imagefilepath = self.transcription_callback(self.transcriptions_to_text(transcriptions, ctx.guild))
        ctx.send(discord.File(imagefilepath))

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
