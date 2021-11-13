import datetime
import random

import discord
from discord import Colour, Embed
from discord.ext import commands
import time
from discord.utils import get
import json

from main import data


class MemberJoinorQuit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("config.json", "r") as config:
            self.data = json.load(config)
            self.channel_join_message = self.data["channel_join_message"]
            self.channel_quit_message = self.data["channel_quit_message"]



    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = get(member.guild.channels, id=self.channel_join_message)
        embed = Embed(title="🔰 **SurfBot** :", timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc),
                      description=f"Bonjour {member.mention} 👋,\n Bienvenue sur SurfrunCraft ! Oublier pas de lire le règlement. \n Nous somme maintenant **{member.guild.member_count}** sur le discord",
                      colour=Colour.dark_blue())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="Développed by Implements#1281", icon_url=self.bot.user.avatar_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = get(member.guild.channels, id=self.channel_quit_message)
        embed = Embed(title="🔰 **SurfBot** :", timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc),
                      description=f"Au revoir {member.mention} 👋.\n Nous somme maintenant **{member.guild.member_count}** sur le discord",
                      colour=Colour.dark_red())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="Développed by Implements#1281", icon_url=self.bot.user.avatar_url)
        await channel.send(embed=embed)

    @commands.command(name="channel_join")
    @commands.has_role(data["support_role_id"])
    async def channel_join(self, ctx):
        channel_id = ctx.channel.id
        self.data["channel_join_message"] = channel_id
        with open("config.json", "w") as config:
            json.dump(self.data, config, indent=4)
        await ctx.message.delete()
        embed = Embed(title="🔧 | Changement de channel", timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc),
                      description=ctx.author.mention + " vous avez bien changer le channel d'arriver.",
                      colour=Colour.dark_green())
        await ctx.channel.send(embed=embed)

    @commands.command(name="channel_quit")
    @commands.has_role(data["support_role_id"])
    async def channeL_quit(self, ctx):
        channel_id = ctx.channel.id
        self.data["channel_quit_message"] = channel_id
        with open("config.json", "w") as config:
            json.dump(self.data, config, indent=4)
        await ctx.message.delete()
        embed = Embed(title="🔧 | Changement de channel", timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc),
                      description=ctx.author.mention + " vous avez bien changer le channel de depart",
                      colour=Colour.dark_red())
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberJoinorQuit(bot))
