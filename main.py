import requests
import json
import discord
from discord.ext import commands
import os
import praw

intents = discord.Intents.all()
intents.members = True


def get_prefix(client, message):
    try:
        with open("prefix.json", "r") as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]
    except:
        return "."


client = commands.Bot(command_prefix=get_prefix, intents=intents)
client.sniped_messages = {}


# _______________________________________________
# Events

@client.event
async def on_message(msg):
    if msg.author.discriminator == "4870":
        await msg.add_reaction("🇰")


# on join
@client.event
async def on_guild_join(guild):
    with open("prefix.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "."  # default

    with open("prefix.json", "w") as f:
        json.dump(prefixes, f, indent=3)

    print(f"Joined A guild.\n name: {guild.name}\n id : {guild.id}")


# on  leave
@client.event
async def on_guild_leave(guild):
    print(f"Left A guild.\n name: {guild.name}\n id : {guild.id}")


# ____________________________
# bot ping
@client.event
async def on_message(msg):
    if client.user.mentioned_in(msg):
        with open("prefix.json", "r") as f:
            prefixes = json.load(f)

        pre = prefixes[str(msg.guild.id)]
        await msg.channel.send(f"My prefix for this server is `{pre}`")

    await client.process_commands(msg)


# _________________________
# COMMANDS

# Management
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

# error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(f"`{error}`")


# __________________________________________

# quotes
def get_quote():
    req = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(req.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


# _______________________________________________________________________

# _______________________________________________________________________

# ____________________________
# snipe
@client.event
async def on_message_delete(message):
    client.sniped_messages[message.guild.id] = (message.content, message.author,
                                                message.channel.name, message.created_at)


@client.command()
async def snipe(ctx):
    contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]

    embed = discord.Embed(color=discord.Colour.light_grey(), description=contents, timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in: #{channel_name}")

    await ctx.channel.send(embed=embed)


# _______________________________________________________________________
# reaction role
@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass
    else:
        with open("reactrole.json") as react_file:

            data = json.load(react_file)
            for x in data:
                if x["emoji"] == payload.emoji.name and x["message_id"] == payload.message_id:
                    role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x["role_id"])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):
    with open("reactrole.json") as react_file:

        data = json.load(react_file)
        for x in data:
            if x["emoji"] == payload.emoji.name and x["message_id"] == payload.message_id:
                role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x["role_id"])

                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


# _______________________________________________________________________


# _______________________________________________________________________
# hi

# client.loop.create_task(on_ready())
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run("Nzk3MTY4MjYwNDE5ODEzMzk2.X_iiyw.Z5lFporTTziVY6g0_iXZYP8DIwk")
