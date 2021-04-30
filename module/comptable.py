from discord.ext import commands

import discord


class Comptable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 501719851740561408:
            c = self.bot.get_channel(833767709522526299)
            mess = await c.history(limit=1).flatten()
            
            for m in mess:
                await c.send(int(m.content)+1)


def setup(bot):
    bot.add_cog(Comptable(bot))


def teardown(bot):
    bot.remove_cog(Comptable(bot))


