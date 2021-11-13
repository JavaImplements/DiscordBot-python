import discord
from discord import Intents
from discord.ext import tasks, commands
from discord.utils import get

from foctions import create_all_channel

import json
import os

description = "descritpion"
desc_status = "desc_status"

with open("config.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]

bot = commands.Bot(command_prefix=prefix, description=description, intents=Intents.all())

bot.remove_command("help")


@bot.event
async def on_ready():
    print("SurfBot :")
    print(" \n")
    print("  - prefix : " + prefix)
    print("  - description : " + description)
    print("  - Status Stream : " + desc_status)

    await create_all_channel(bot)
    await bot.change_presence(status=discord.Status.do_not_disturb,
                              activity=discord.Game(f"prefix: {prefix}| Développeur : Implements#1281"))
    update_channel.start()


@tasks.loop(seconds=2.0)
async def update_channel():
    reload_member = False
    reload_boost = False
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if str(channel.name).startswith("» Membres"):
                await channel.edit(name="» Membres " + str(guild.member_count), reason=" reload channel")
                reload_member = True
            if str(channel.name).startswith("» Boosts"):
                await channel.edit(name="» Boosts " + str(guild.premium_subscription_count), reason="reload channel")
                reload_boost = True

        if not reload_member:
            overwrites_member_channel = {
                get(guild.roles, name="@everyone"): discord.PermissionOverwrite(connect=False),
            }
            await guild.create_voice_channel(name="» Membres " + str(guild.member_count),
                                             overwrites=overwrites_member_channel)
        if not reload_boost:
            overwrites_boost_channel = {
                get(guild.roles, name="@everyone"): discord.PermissionOverwrite(connect=False),
            }
            await guild.create_voice_channel(name="» Boosts " + str(guild.premium_subscription_count),
                                             overwrites=overwrites_boost_channel)


for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        print(f"L'extension {filename} à bien été charger.")
        bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    bot.run(token, bot=True)
