import time
import datetime

import discord
from discord.ext import commands
from discord.utils import get
import json


def is_mute(guild, userid):
    target = get(guild.members, id=userid)
    if target is None:
        return "Non"

    if get(target.roles, name="Muted") is None:
        return "Oui"
    else:
        return "Non"



class CommandSanction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("warn.json", "r") as f:
            self.warns = json.load(f)

    def reload_warnfile(self):
        with open("warn.json", "r") as f:
            self.warns = json.load(f)

    async def is_ban(self, guild, userid):

        bans = await guild.bans()
        user = await self.bot.fetch_user(userid)
        if user in bans:
            return "Oui"
        else:
            return "Non"

    def warn(self, userid):
        self.reload_warnfile()
        if userid not in self.warns:
            return "0"
        warn = self.warns[userid]["warn"]

        return str(warn)

    # TODO: faire un jolie truc
    @commands.command(name="sanction")
    async def sanctions(self, ctx, target):
        isban = await self.is_ban(guild=ctx.guild, userid=target)
        member = await ctx.guild.fetch_member(target)
        embed = discord.Embed(title="🚨 | **SurfBot Sanctions** : ", colour=discord.Colour.blue(), timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc))
        embed.add_field(name="Mute :", value=is_mute(ctx.guild, target), inline=True)
        embed.add_field(name="Ban :", value=isban, inline=True)
        embed.add_field(name="Warns:", value=self.warn(target), inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="Développed by Implements#1281", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CommandSanction(bot))
