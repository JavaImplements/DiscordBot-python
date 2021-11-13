import time
import datetime

import discord
from discord.ext import commands
from discord.utils import get
import json


class CommandWarn(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("warn.json", "r") as f:
            self.warns = json.load(f)

    async def warn_embed(self, userid, guild):
        member = await guild.fetch_member(userid)
        embed = discord.Embed(title="🚨 | Warn avec succée", colour=discord.Colour.green(), timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc))
        embed.add_field(name="Identifiant :", value=userid, inline=True)
        embed.add_field(name="Pseudo :", value=member.mention, inline=True)
        embed.add_field(name="Warn :", value=self.warns[userid]["warn"], inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="Développed by Implements#1281", icon_url=self.bot.user.avatar_url)
        return embed

    @commands.command(name="warn")
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, userid):
        userid = str(userid)
        if not userid in self.warns:
            self.warns[userid] = {}
            self.warns[userid]["warn"] = 1
            with open("warn.json", "w") as f:
                json.dump(self.warns, f, indent=4)
            await ctx.send(embed=await self.warn_embed(userid=userid, guild=ctx.guild))
            return
        self.warns[userid]["warn"] = str(int(self.warns[userid]["warn"]) + 1)
        with open("warn.json", "w") as f:
            json.dump(self.warns, f, indent=4)
        await ctx.send(embed=await self.warn_embed(userid=userid, guild=ctx.guild))


def setup(bot):
    bot.add_cog(CommandWarn(bot))
