import discord
from discord.ext import commands
import asyncio
import random

class On_Ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global num_servers
        global servers
        await self.client.wait_until_ready()
        print("\n", "_" * 20)
        if self.client.is_closed:
            servers = []
            for server in self.client.guilds:
                servers.append(server.name)
            print("\nCurrent Servers   :", *servers, sep="\n\t\t\t\t\t")
            num_servers = len(servers)
            print("Number of Servers :", num_servers)

        status_type = [discord.ActivityType.watching, discord.ActivityType.listening]
        status = [f"{num_servers} Important GUILDS", "560 users"]
        await self.client.change_presence(
            activity=discord.Activity(type=random.choice(status_type), name=random.choice(status)))


        print("Bot Is Ready!")
        print(f"Logged in as      : {self.client.user.name}")
        print(f"With the iD       : {self.client.user.id}")
        print("_____________________")





def setup(client):
    client.add_cog(On_Ready(client))
