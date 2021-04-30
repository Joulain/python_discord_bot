from discord.ext import commands

import discord


class Trickster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, aliases=["gp"])
    @commands.is_owner()
    async def get_position(self, ctx):
        guild = self.bot.get_guild(373034685695000576)
        for r in guild.roles:
            print(r, r.position, sep=":")

    
    @commands.command(pass_context=True, aliases=["ms"])
    @commands.is_owner()
    async def make_separate(self, ctx):
        guild = self.bot.get_guild(373034685695000576)
        role = discord.utils.get(guild.roles, name="The trickster is back")
        await role.edit(name="The trickster is back once again", hoist=True)


def setup(bot):
    bot.add_cog(Trickster(bot))


def teardown(bot):
    bot.remove_cog(Trickster(bot))