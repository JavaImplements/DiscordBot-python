import time
import datetime

from discord.ext import commands
from discord import Embed, Colour


class CommandDebug(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="debug")
    @commands.has_permissions(administrator=True)
    async def commandName(self, ctx):
        count_member = ctx.guild.member_count
        embed = Embed(title="test", colour=Colour.red(), description="test",
                      timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc))
        embed.add_field(name="2", value="||test||")
        embed.set_author(name="author", url=ctx.author.avatar_url)
        embed.set_footer(text="footer", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CommandDebug(bot))
