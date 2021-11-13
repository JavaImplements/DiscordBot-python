import time
import datetime

from discord.ext import commands
from discord import Embed, Colour
from discord.utils import get
import discord
import os
import json

from main import data


class SystemTickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("config.json", 'r') as config:
            self.data = json.load(config)

    @commands.command(name="ticket-setup")
    @commands.has_role(data["support_role_id"])
    async def ticket_setup(self, ctx):
        await ctx.message.delete()
        embed_ticket = Embed(title="🌀 | **SurfBot** Tickets :", colour=Colour.dark_green())
        embed_ticket.add_field(name="Création de tickets",
                               value="Bonjour, Vous avez un problème ? Vous avez juste à crée un ticket en réagissant avec l'emoji 📩")
        embed_ticket.set_thumbnail(url=self.bot.user.avatar_url)
        embed_ticket.set_footer(text="Développed by Implements#1281")

        message = await ctx.send(embed=embed_ticket)

        await message.add_reaction("📩")

        self.data["channel_id_ticket"] = ctx.channel.id
        self.data["message_id_ticket"] = message.id
        with open("config.json", "w") as config:
            json.dump(self.data, config, indent=4)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member.id != self.bot.user.id:
            if payload.emoji.name == "📩":
                message_id = payload.message_id
                channel = get(self.bot.get_guild(payload.guild_id).channels, id=payload.channel_id)
                message = await channel.fetch_message(message_id)
                await message.remove_reaction(payload.emoji, payload.member)
                if payload.member.id != self.bot.user.id:
                    if message_id == int(self.data["message_id_ticket"]):
                        if not get(self.bot.get_guild(payload.guild_id).channels,
                                   name="support-" + str(payload.member.name).lower() + "-" + str(payload.member.id)):

                            embed = Embed(title="🌀 | **SurfBot** Tickets :", colour=Colour.dark_green(), timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc))
                            embed.add_field(name="✅ Création du tickets..",
                                            value="Votre ticket à bien été crée, Posé vos question dans le channel qui à été crée")
                            embed.set_thumbnail(url=self.bot.user.avatar_url)
                            embed.set_footer(text="Développed by Implements#1281")
                            await payload.member.send(embed=embed)

                            overwrites = {
                                get(self.bot.get_guild(payload.guild_id).roles,
                                    name="Support"): discord.PermissionOverwrite(
                                    read_messages=True),
                                get(self.bot.get_guild(payload.guild_id).roles,
                                    name="@everyone"): discord.PermissionOverwrite(
                                    read_messages=False),
                                get(self.bot.get_guild(payload.guild_id).members,
                                    id=payload.member.id): discord.PermissionOverwrite(
                                    read_messages=True),

                            }
                            # Création du channel
                            channel = await self.bot.get_guild(payload.guild_id).create_text_channel(
                                'support-' + payload.member.name + "-" + str(payload.member.id), overwrites=overwrites)

                            embed_channel = Embed(title="🌀 | **SurfBot** Tickets :", colour=Colour.dark_green(), timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc))
                            embed_channel.add_field(
                                name=f"Bonjour, " + str(
                                    payload.member.name).lower() + " votre ticket à correctement été créé.",
                                value=f"Vous pouvez des maintenant nous notifier votre problème et un membre du staff s'occupera de vous le plus rapidement possible",
                                inline=False)
                            embed_channel.set_thumbnail(url=self.bot.user.avatar_url)
                            embed_channel.set_footer(text="Développed by Implements#1281")
                            await channel.send(embed=embed_channel)

                            fichier = open('tickets-logs/' + 'support-' + payload.member.name + "-" + str(
                                payload.member.id) + ".txt", 'a')
                            fichier.write(payload.member.name + " à crée se ticket \n -------------- ")
                            fichier.close()
                        else:

                            embed = Embed(title="🌀 | **SurfBot** Tickets :", colour=Colour.red(), timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc))
                            embed.add_field(name="🚫 Erreur", value="Vous avez déjà un ticket ouvert !")
                            embed.set_thumbnail(url=self.bot.user.avatar_url)
                            embed.set_footer(text="Développed by Implements#1281")
                            await payload.member.send(embed=embed)

    @commands.command(name="ticket-close")
    @commands.has_role(data["support_role_id"])
    async def ticket_close(self, ctx):
        channel_name = str(ctx.channel.name)

        if channel_name.startswith("support-"):
            channel_name = str(ctx.channel.name).split("-")
            id_user = int(channel_name[2])
            target = await ctx.guild.fetch_member(id_user)

            channel_log = get(ctx.guild.channels, name="ticket-log")

            await channel_log.send(file=discord.File("tickets-logs/" + ctx.channel.name + ".txt"))
            os.remove("tickets-logs/" + ctx.channel.name + ".txt")

            await ctx.channel.delete()

            embed = Embed(title="🌀 | **SurfBot** Tickets :", colour=Colour.red(), timestamp=datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc))
            embed.add_field(name="Ticket supprimer", value="Votre ticket à été supprimer !")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text="Développed by Implements#1281")
            await target.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author

        if isinstance(message.channel, discord.channel.TextChannel):

            channel_name = message.channel.name

            if member.id != self.bot.user.id:
                if str(message.content) != "!ticket-close":
                    if channel_name.startswith("support-"):
                        fichier = open('tickets-logs/' + channel_name + ".txt", 'a')
                        fichier.write(member.name + " : " + message.content + "\n")
                        fichier.close()


def setup(bot):
    bot.add_cog(SystemTickets(bot))
