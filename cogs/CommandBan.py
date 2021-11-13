import time
import datetime

import discord
from discord.ext import commands
from discord.utils import get


class CommandBan(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, userid):
        userid = str(userid)
        member = get(ctx.guild.members, id=int(userid))
        if member is not None:
            await ctx.guild.ban(member)
            await ctx.send(embed=discord.Embed(title="🚨 | Bannie avec succée", timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc),
                                               description=f"{member.mention} à été bannie du serveur. 🔨",
                                               colour=discord.Colour.red()))


def setup(bot):
    bot.add_cog(CommandBan(bot))
