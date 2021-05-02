from past import file_writer as fw 
from discord.ext import commands

import discord


class Monitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            pass
        else:
            if message.author.id == 501719851740561408:
                c = self.bot.get_channel(833767709522526299)
                mess = await c.history(limit=1).flatten()
                for m in mess:

                    await c.send(int(m.content)+1)

            if message.channel.category is None:
                category = "nocategory"
                category_id = "nocatid"
            else:
                category = message.channel.category 
                category_id = message.channel.category.id

            msg = "\"{0.author.display_name}\" aka {0.author} {{{0.author.id}}} : {0.content} ({0.id})".format(message)
            msg_live = "[{0.guild}] <{1}> {{{0.channel}}} - \"{0.author.display_name}\" aka {0.author} : {0.content} ({0.id})".format(message, category)

            for i in message.attachments:
                msg = msg + " - {0}".format(i.url)
                msg_live = msg_live + " - {0}".format(i.url)

            msg = msg + "\n"
            msg_live = msg_live + "\n"

            guild_folder = "{0.guild}_{0.guild.id}".format(message)
            category_folder = f"{category}_{category_id}"
            file = "{0.channel}_{0.channel.id}".format(message)
            fw.file_writer(guild_folder,category_folder,file,msg)

            fw.full_writer(msg_live)


    @commands.Cog.listener()
    async def on_raw_message_delete(self, ctx):
        if not ctx.cached_message:
            if not ctx.guild_id:
                pass
            else:
                guild = self.bot.get_guild(ctx.guild_id)
                channel = self.bot.get_channel(ctx.channel_id)

                msg = "an old message has been deleted\n"
                msg_live = "[{0}] <raw> {{{1}}} an old message was deleted\n".format(guild, channel)

                guild_folder = "{0}_{0.id}".format(guild)
                category_folder = "raw"
                file = "{0}_{0.id}".format(channel)
                fw.file_writer(guild_folder, category_folder, file, msg)

                fw.full_writer(msg_live)

        else:
            if not ctx.guild_id:
                pass
            else:

                msg = "\"{0.author.display_name}\" aka {0.author} {{{0.author.id}}} : {0.content} ({0.id}) was deleted\n".format(ctx.cached_message)
                if ctx.cached_message.channel.category is None:
                    category = "nocategory"
                    category_id = "nocatid"
                else:
                    category = ctx.cached_message.channel.category
                    category_id = ctx.cached_message.channel.category.id
                msg_live = "[{0.guild}] <{1}> {{{0.channel}}} - \"{0.author.display_name}\" aka {0.author} : {0.content} ({0.id}) was deleted\n"\
                .format(ctx.cached_message, category)

                guild_folder = "{0}_{0.id}".format(ctx.cached_message.guild)
                category_folder = "{0}_{1}".format(category, category_id)
                file = "{0}_{0.id}".format(ctx.cached_message.channel)
                fw.file_writer(guild_folder, category_folder, file, msg)

                fw.full_writer(msg_live)


    @commands.Cog.listener()
    async def on_raw_message_edit(self, ctx):
        if not ctx.cached_message:
            if "guild_id" not in ctx.data:
                pass
            else:
                guild = self.bot.get_guild(int(ctx.data["guild_id"]))
                channel = self.bot.get_channel(int(ctx.data["channel_id"]))

                msg = "a message has been modified into : {0[content]}\n".format(ctx.data)
                msg_live = "[{0}] <raw> {{{1}}} a message has been modified into : {2[content]} ({2[id]})\n".format(guild, channel, ctx.data)

                guild_folder = "{0}_{0.id}".format(guild)
                category_folder = "raw"
                file = "{0}_{0.id}".format(channel)
                fw.file_writer(guild_folder, category_folder, file, msg)

                fw.full_writer(msg_live)
        else:
            if "guild_id" not in ctx.data:
                pass
            else:
                category = discord.utils.get(ctx.cached_message.guild.channels, id=ctx.cached_message.channel.category_id)

                msg = "\"{0.author.display_name}\" aka {0.author} {{{0.author.id}}} : {0.content} was changed into : {1[content]} ({0.id})\n"\
                .format(ctx.cached_message, ctx.data)
                msg_live = "[{0.guild}] <{1}> {{{0.channel}}} - \"{0.author.display_name}\" aka {0.author} : {0.content} was changed into : {2[content]}\n"\
                .format(ctx.cached_message, category, ctx.data)

                guild_folder = "{0}_{0.id}".format(ctx.cached_message.guild)
                category_folder = "{0}_{1}".format(category, ctx.cached_message.channel.category_id)
                file = "{0}_{0.id}".format(ctx.cached_message.channel)
                fw.file_writer(guild_folder, category_folder, file, msg)

                fw.full_writer(msg_live)


def setup(bot):
    bot.add_cog(Monitor(bot))


def teardown(bot):
    bot.remove_cog(Monitor(bot))


