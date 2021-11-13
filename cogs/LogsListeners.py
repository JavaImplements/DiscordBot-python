import time
import datetime

from discord.ext import commands
from discord import Embed, Colour
from discord.utils import get
import json

from main import data


class LogsListeners(commands.Cog):
    """
        - quand une personne edite un message 🚫
        - Log les message supprimer ✅
    """

    def __init__(self, bot):
        self.bot = bot
        with open("config.json", "r") as config:
            self.data = json.load(config)
            self.logs_channel = self.data["logs_channel"]

    @commands.command(name="logs_channel")
    @commands.has_role(data["support_role_id"])
    async def set_logs_channel(self, ctx):
        channel_id = ctx.channel.id
        self.data["logs_channel"] = channel_id
        with open("config.json", "w") as config:
            json.dump(self.data, config, indent=4)

        embed = Embed(title="🔧 | Changement de channel",
                      description=ctx.author.mention + " vous avez bien changer le channel des logs.",
                      colour=Colour.dark_green())
        await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel_log = get(message.guild.text_channels, id=self.data["logs_channel"])

        if channel_log is not None:
            embed = Embed(title="💈 | Logs", colour=Colour.dark_red(), timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc))
            embed.add_field(name="🔧 Message supprimer",
                            value=f"Le message de {message.author.mention} à été supprimer dans {message.channel.mention} \n 📝 | **__Message__** : {message.content}")
            embed.set_footer(text=f"ID Message : {message.id}")
            await channel_log.send(embed=embed)

    """
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel_log = get(before.guild.text_channels, id=self.data["logs_channel"])

        if channel_log is not None:
            embed = Embed(title="💈 | Logs", colour=Colour.dark_red())
            embed.add_field(name="Message édité",
                            value=f"{before.author.mention} à édité un message \n __**Avent__** : " + str(before.content) + " \n __**Après**__ : " + str(after.content) + "")
            embed.set_footer(text=f"ID Message : {before.id}")
            await channel_log.send(embed=embed)
    """


def setup(bot):
    bot.add_cog(LogsListeners(bot))
