import discord
from discord.ext import commands
import os


class reloadCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload")
    @commands.has_permissions(administrator=True)
    async def commandName(self, ctx, args):
        if args is not None:
            self.bot.reload_extension(f'cogs.{args[:-3]}')
            await ctx.send(f"✅ L'extension {args} à bien été reload.")
        else:
            for filename in os.listdir("./cogs"):
                if filename.endswith('.py'):
                    self.bot.reload_extension(f'cogs.{filename[:-3]}')
                    await ctx.send(f"✅ L'extension {filename} à bien été reload.")


def setup(bot):
    bot.add_cog(reloadCommand(bot))
