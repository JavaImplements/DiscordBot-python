import time

import discord
from discord.ext import commands
from discord.utils import get
import datetime
from time import gmtime, strftime
from time import strftime
import json

from main import data


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # # # # # # # # #
    #                  #
    #       MUTE       #
    #                  #
    # # # # # # # # #

    async def set_mute(self, ctx, role: discord.Role, target: discord.Member, reason):

        await target.add_roles(role, reason=f"{target.name} à été mute par {ctx.author.name}")

        embed_mute = discord.Embed(title="🔰 **SurfBot Modération** :", colour=discord.Colour.red())
        embed_mute.add_field(name="🔹 __**Membre mute**__ : ", value=f"Le membre {target.name} à été mute !",
                             inline=False)
        embed_mute.add_field(name="🔹 __**Reason**__ : ", value=str(reason), inline=False)
        embed_mute.add_field(name="🔹 __**Mute par**__ : ", value=f"{ctx.author.name}", inline=False)
        embed_mute.add_field(name="🔹 __**Date**__ : ", value=f"{datetime.now()}", inline=False)
        embed_mute.set_thumbnail(url=target.avatar_url)
        embed_mute.set_footer(text="Développed by Implements#1281")

        await ctx.send(embed=embed_mute)

    @commands.command(name="mute")
    @commands.has_role(data["support_role_id"])
    async def mute(self, ctx, target: discord.Member, *, reason="Aucune reason n'as été donner"):
        await ctx.message.delete()
        if target is not None:
            muted_role = get(ctx.guild.roles, name="Muted")
            if muted_role is None:
                role = await ctx.guild.create_role(name="Muted",
                                                   permissions=discord.Permissions(send_messages=False, speak=False),
                                                   reason=reason)
                for channel in ctx.guild.channels:
                    await channel.set_permissions(role, send_messages=False, speak=False)
                await target.add_roles(role, reason=f"{target.name} à été mute par {ctx.author.name}")

                await self.set_mute(ctx, role, target, reason)

            else:
                await target.add_roles(muted_role, reason=f"{target.name} à été mute par {ctx.author.name}")

                await self.set_mute(ctx, muted_role, target, reason)

    # # # # # # # # #
    #                 #
    #     UN MUTE     #
    #                 #
    # # # # # # # # #

    @commands.command(name="unmute")
    @commands.has_role(data["support_role_id"])
    async def unmute(self, ctx, target: discord.Member):
        role = get(target.roles, name="Muted")
        await ctx.message.delete()
        if role is not None:
            embed = discord.Embed(title="🔰 **SurfBot Modération** :", colour=discord.Colour.green(), timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc))
            embed.add_field(name="🔹 __**Membre unmute**__ : ", value=f"Le Membre {target.name} à été unmute",
                            inline=False)
            embed.add_field(name="🔹 __**Par**__ : ", value=ctx.author.name, inline=False)
            embed.add_field(name="🔹 __**Date**__ : ", value=datetime.now(), inline=False)
            embed.set_thumbnail(url=target.avatar_url)
            embed.set_footer(text="Développed by Implements#1281")

            await ctx.send(embed=embed)
            await target.remove_roles(role, reason=f"{target.name} à été unmute par" + ctx.author.name)
        else:

            await ctx.send(embed=discord.Embed(title=f"**Erreur : Le Membre {target.name} n'est pas mute**",
                                               colour=discord.Colour.red(), timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)), delete_after=3)



def setup(bot):
    bot.add_cog(Moderation(bot))
