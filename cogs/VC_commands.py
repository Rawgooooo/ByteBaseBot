import discord
from discord.ext import commands

class VC_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
# _______________________________________

    # Vc
    @commands.command(pass_context=True)
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send(":red_circle: You must be connected to a voice channel.")

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("I left the voice channel.")
        else:
            await ctx.send("I was never connected to a VC!")
    # ______________________________
# ________________________________________

def setup(client):
    client.add_cog(VC_commands(client))
