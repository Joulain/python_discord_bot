#!/usr/bin/env python3

from ressources import file_reader as fr
from discord.ext import commands
from subprocess import call

import discord
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='m! ', intents=intents)
bot.remove_command('help')


for filename in os.listdir('./module'):
    if filename.endswith('.py'):
        bot.load_extension(f'module.{filename[:-3]}')


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(f"module.{extension}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.channel.send("This extension is already loaded")
    except commands.ExtensionNotFound:
        await ctx.channel.send("I could not find the extension you tried to load")
    except commands.ExtensionFailed:
        await ctx.channel.send("I failed to load the extension !")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f"module.{extension}")
    except commands.ExtensionNotLoaded:
        await ctx.channel.send("This extension was not loaded")
    except commands.ExtensionNotFound:
        await ctx.channel.send("I could not find the extension you tried to unload")


@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.channel.send("You must be the owner to use this command.")
        print(error)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("You must tell me which extension to load")
        print(error)
    else:
        await ctx.channel.send("An error as occured, please contact the bot owner")
        print(error)


@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.channel.send("You must be the owner to use this command.")
        print(error)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("You must tell me which extension to unload")
        print(error)
    else:
        await ctx.channel.send("An error as occured, please contact the bot owner")
        print(error)


@bot.command()
@commands.is_owner()
async def restart(ctx):
    call("./reboot.sh")


@bot.event
async def on_ready():
    bot_name = bot.user.name
    bot_id = bot.user.id
    package_version = discord.__version__

    msg = "\nLogged in as: {0} - {1} \nVersion: {2} \n".format(bot_name, bot_id, package_version)

    print(msg, "Successfully running")


bot.run(fr.TOKEN)