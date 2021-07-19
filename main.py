import requests
import json
import discord
from discord.ext import commands
import os
import praw
from discord_slash import SlashCommand
from discord.ext.commands import CommandNotFound


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
slash = SlashCommand(client, sync_commands=True)

# _______________________________________________
# Events

@client.event
async def on_message(msg):
    if msg.author.discriminator == "4870":
        await msg.add_reaction("🇰")

# bot prefix
@client.event
async def on_guild_join(guild):
    with open("prefix.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "."  # default

    with open("prefix.json", "w") as f:
        json.dump(prefixes, f, indent=3)


# ____________________________
# bot ping
@client.event
async def on_message(msg):
    if client.user.mentioned_in(msg):
        with open("prefix.json", "r") as f:
            prefixes = json.load(f)

        pre = prefixes[str(msg.guild.id)]
        await msg.channel.send(f"My prefix for this server is '{pre}'")

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
        await ctx.send(error)
    print(error)

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
snipe_message_content = []
snipe_message_author = []


@client.event
async def on_message_delete(message):
    snipe_message_content.append(message.content)
    snipe_message_author.append(message.author.name)
    name = snipe_message_author


@client.command()
async def snipe(message):
    if snipe_message_content == None:
        await message.channel.send("Theres nothing to snipe.")
    else:
        embed = discord.Embed(description=f"{snipe_message_content}")
        embed.set_footer(text=f"Asked by {message.author.name}#{message.author.discriminator}",
                         icon_url=message.author.avatar_url)
        embed.set_author(name=f"@{snipe_message_author}")
        await message.channel.send(embed=embed)
        return


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
