
from discord.ext import commands
from discord import Embed, Colour
import datetime
import time

class CommandHelp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def commandName(self, ctx):
        embed = Embed(title="🤖 | **Help** :", colour=Colour.dark_theme(), timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc))
        embed.add_field(name=f" {self.bot.command_prefix}channel_join", value=f"Channel de bienvenue.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}channel_quit", value=f"Channel de dépard.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}mute", value=f"mute un membre.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}tempmute 🚫", value=f"mute un membre pendant un temps.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}unmute", value=f"unmute un membre.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}ban ", value=f"ban un membre.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}tempban 🚫", value=f"ban un membre pendant un temps.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}warn ", value=f"warn un membre.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}sanction ⏳", value=f"les sanctions d'un membre.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}ticket-setup", value=f"Mettre en place les tickets.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}ticket-close", value=f"Fermer un ticket.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}reload", value=f"reload une cogs.", inline=True)
        embed.add_field(name=f" {self.bot.command_prefix}logs_channel", value=f"Channel des logs.", inline=True)
        embed.add_field(name="\n‌‌ \n__Pourquoi il y as des emoji sur des commands ?__\n", value="\n‌‌ \n🚫 : En cours de développement \n 🔧 : Fonctionne mal, bug ou est bientôt finit\n  ⏳ : en test... \n", inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text="Développed by Implements#1281", icon_url=self.bot.user.avatar_url)
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(CommandHelp(bot))