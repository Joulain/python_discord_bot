from discord.ext import commands
from gtts import gTTS


import discord
import asyncio
import os


class NoTts(commands.CheckFailure):
    pass


def NTts():
    async def checker(ctx):
        c = False
        for m in ctx.guild.members:
            for r in m.roles:
                if str(r) == "tts":
                    c = True
        if c:
            raise NoTts("Someone already have the tts role on the serveur")
        return True
    return commands.check(checker)


class Tts(commands.Cog):
    def __init__(self, bot):
            self.bot = bot
            self.bot.ch_tts = None
            self.bot.language = 'fr'
            self.bot.vc = None
            self.bot.playlist = []


    async def play_next(self, ctx):
        while len(self.bot.playlist) > 0:

            self.bot.vc.play(discord.FFmpegPCMAudio(self.bot.playlist[0]), after=lambda e:print('done', e))
            while self.bot.vc.is_playing():
                await asyncio.sleep(1)

            os.remove(self.bot.playlist[0])
            self.bot.playlist.pop(0)


    @commands.Cog.listener()
    async def on_message(self,ctx):
        if self.bot.ch_tts is not None:
            if ctx.channel == self.bot.ch_tts:
                if ctx.content.startswith("m! "):
                    pass
                else:
                    my_text = ctx.author.display_name + " à dit " + ctx.content
                    path = "ressources/audio_files/{0}.mp3".format(my_text)

                    while os.path.isfile(path):
                        path = path.split(".")[0] + "1.mp3"
                    myobj = gTTS(text=my_text, lang=self.bot.language, slow=False)
                    myobj.save(path)
                
                    self.bot.playlist.append(path)
                    await self.play_next(ctx)

    
    @commands.command(pass_context=True, aliases=["tts"])
    @commands.guild_only()
    @NTts()
    async def text_to_speech(self, ctx):    
        if not ctx.message.author.voice:
            msg = f"You have to be in a voice channel to use this command {ctx.message.author.mention}"
            await ctx.channel.send(msg)
        else:
            if not discord.utils.get(ctx.guild.roles, name="tts"):
                role = await ctx.guild.create_role(name="tts")
            else:
                role = discord.utils.get(ctx.guild.roles, name="tts")
            everyone = discord.utils.get(ctx.guild.roles, name="@everyone")
            await ctx.message.author.add_roles(role)
            self.bot.vc = await ctx.message.author.voice.channel.connect()

            ch_typo = "tts_muted"
            self.bot.ch_tts = await ctx.guild.create_text_channel(ch_typo)
            await self.bot.ch_tts.set_permissions(everyone, view_channel=False)
            await self.bot.ch_tts.set_permissions(role, view_channel=True)


    @commands.command(pass_context=True, aliases=["atts"])
    @commands.guild_only()
    @commands.has_role("tts")
    async def add_text_to_speech(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="tts")
        await member.add_roles(role)

    
    @commands.command(pass_context=True, aliases=["rtts"])
    @commands.guild_only()
    @commands.has_role("tts")
    async def remove_text_to_speech(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="tts")
        await member.remove_roles(role)


    @commands.command(pass_context=True, aliases=["stts"])
    @commands.guild_only()
    @commands.has_role("tts")
    async def stop_text_to_speech(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="tts")
        msg = "quitting"
        await ctx.channel.send(msg)

        for m in ctx.guild.members:
            for r in m.roles:
                if str(r) == "tts":
                    await m.remove_roles(role)

        await ctx.guild.voice_client.disconnect()

        if self.bot.ch_tts is not None:
            await self.bot.ch_tts.delete()
        else:
            print("channel is none")


    @text_to_speech.error
    async def tts_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.channel.send("This command must be use on a discord server")
            print(error)
        elif isinstance(error, NoTts):
            await ctx.channel.send("The tts function is already used on this server")
            print(error)
        else:
            print(error)


    @stop_text_to_speech.error
    async def stts_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.channel.send("This command must be use on a discord server")
            print(error)
        elif isinstance(error, commands.MissingRole):
            await ctx.channel.send("You must have the tts role")
            print(error)
        else:
            print(error)


    @add_text_to_speech.error
    async def atts_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.channel.send("This command must be use on a discord server")
            print(error)
        elif isinstance(error, commands.MissingRole):
            await ctx.channel.send("You must have the tts role")
            print(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("You must tell me who to add")
            print(error)
        elif isinstance(error, commands.MemberNotFound):
            await ctx.channel.send("I could not find the member")
            print(error)
        elif isinstance(error, commands.BadArgument):
            await ctx.channel.send("I did not understand who i needed to add\nPlease tag the user you want me to add")
            print(error)
        else:
            await ctx.channel.send("An error as occured, please contact the bot owner")
            print(error)


    @remove_text_to_speech.error
    async def rtts_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.channel.send("This command must be use on a discord server")
            print(error)
        elif isinstance(error, commands.MissingRole):
            await ctx.channel.send("You must have the tts role")
            print(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("You must tell me who to add")
            print(error)
        elif isinstance(error, commands.MemberNotFound):
            await ctx.channel.send("I could not find the member")
            print(error)
        elif isinstance(error, commands.BadArgument):
            await ctx.channel.send("I did not understand who i needed to add\nPlease tag the user you want me to add")
            print(error)
        else:
            await ctx.channel.send("An error as occured, please contact the bot owner")
            print(error)


def setup(bot):
    bot.add_cog(Tts(bot))


def teardown(bot):
    bot.remove_cog(Tts(bot))


