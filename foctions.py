import discord
from discord.utils import get


async def create_all_channel(bot):
    for guild in bot.guilds:
        print(guild.name)
        if get(guild.channels, name="ticket-log") is None:
            print("DEBUG : Le channel 'ticket-log' n'existe pas. Il vas être créé")
            overwrites = {
                get(guild.roles, name="Support"): discord.PermissionOverwrite(read_messages=True),
                get(guild.roles, name="@everyone"): discord.PermissionOverwrite(read_messages=False),
            }
            channel = await guild.create_text_channel('ticket-log', overwrites=overwrites)
            await channel.send("🌀 : Je vous est créé ce channel qui regroupera tout les log de tout les tickets ")
            print("DEBUG : la creation du channel 'ticket-log' est ✅")
