import discord
from discord.ext import commands

class VC_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
# _______________________________________

    # Vc
    @commands.command(help="Join your vc")
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(help="Leave vc")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
    # ______________________________
# ________________________________________

def setup(client):
    client.add_cog(VC_commands(client))
