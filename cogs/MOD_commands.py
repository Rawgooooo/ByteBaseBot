import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import json
import datetime
import asyncio
import random


class MOD_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        DiscordComponents(client)

    # _______________________________________________________

    # add_role
    @commands.command(aliases=["ADDROLE", "arole", "AROLE"])
    @has_permissions(manage_roles=True)
    async def addrole(self, ctx, role: discord.Role, member: discord.Member):
        await member.add_roles(role)

        em = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                           title=f"Promote!! - {member}")
        em.add_field(name="Role given:", value=f"{member.mention} was give {role}-role by {ctx.author.mention}")
        em.set_thumbnail(url=member.avatar_url)
        em.set_footer(text=f"{member} Congrats!!!")
        await ctx.send(embed=em)

        embed = discord.Embed(colour=discord.Colour.gold(), timestamp=ctx.message.created_at,
                              title=f"User Roles - {member}")
        roles = [role for role in member.roles]
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"{member}'s new roles!")
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Roles:", value="".join([role.mention for role in roles]), inline=False)
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.send(embed=embed)

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'{ctx.message.author.mention} You do not have the permission to run that command! :red_circle:')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.message.author.mention} There is an Argument missing in that command! :red_circle:\nAddrole Command Syntax: .addrole @role @user ')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f'{ctx.message.author.mention} To give role to someone you need to mention them! :red_circle:\nAddrole Command Syntax: .addrole @role @user ')
        else:
            await ctx.send(
                'There was an error while executing the command! Boss has been informed! :red_circle:')
            await ctx.send(error)

    # ______________________________

    # del_role
    @commands.command(aliases=["rrole", "RROLE"])
    @has_permissions(manage_roles=True)
    async def removerole(self, ctx, role: discord.Role, member: discord.Member):
        await member.remove_roles(role)

        em = discord.Embed(colour=discord.Colour.dark_red(), timestamp=ctx.message.created_at,
                           title=f"Demote!! - {member}")
        em.add_field(name="Role Removed:",
                     value=f"{member.mention} was demoted by {ctx.author.mention}. ({role}-role was removed!!)")
        em.set_thumbnail(url=member.avatar_url)
        em.set_footer(text=f"{member} Better luck nxt time!")
        await ctx.send(embed=em)

        embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                              title=f"User Roles - {member}")
        roles = [role for role in member.roles]
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"{member}'s current roles.")
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Roles:", value="".join([role.mention for role in roles]), inline=False)
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.send(embed=embed)

    @removerole.error
    async def removerole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'{ctx.message.author.mention} You do not have the permission to run that command! :red_circle:')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.message.author.mention} There is an Argument missing in that command! :red_circle:\nRemove_role Command Syntax: .removerole @role @user ')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f'{ctx.message.author.mention} To give role to someone you need to mention them! :red_circle:\nRemove_role Command Syntax: .removerole @role @user ')
        else:
            await ctx.send(
                'There was an error while executing the command! Boss has been informed! :red_circle:')
            print(error)

    # ______________________________

    # react_role
    @commands.command(aliases=["REACTROLE", "rr", "RR"])
    @has_permissions(manage_roles=True)
    async def reactrole(self, ctx, emoji: discord.Emoji, role: discord.Role, *, message):
        embed = discord.Embed(description=message)
        msg = await ctx.channel.send(embed=embed)
        await msg.add_reaction(emoji)

        with open("reactrole.json") as json_file:
            data = json.load(json_file)

            new_react_role = {
                "role_name": role.name,
                "role_id": role.id,
                "emoji": emoji.name,
                "message_id": msg.id
            }

            data.append(new_react_role)

        with open("reactrole.json", "w") as j:
            json.dump(data, j, indent=4)

    @reactrole.error
    async def rr_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'{ctx.message.author.mention} You do not have the permission to run that command! :red_circle:')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.message.author.mention} There is an Argument missing in that command! :red_circle:\nReactrole Command Syntax: .rr <emoji> <@role> message ')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f'{ctx.message.author.mention} :red_circle:\nReactrole Command Syntax: .rr <emoji> <@role> message ')
        else:
            await ctx.send(
                'There was an error while executing the command! Boss has been informed! :red_circle:')
            print(error)

    # ______________________________

    # announcement
    @commands.command()
    async def announce(self, ctx, *, msg):
        channel = ctx.channel
        try:
            title = msg.split(",")[0]
            dsc = msg.split(",")[1]
            name, content = dsc.split(" . ")
            footer = msg.split("/ ")[1]
            # txt = f"{title}\n\nReact with:\n✅ for {name} \nor \n❌ for {content}"
        except:
            await channel.send("Correct Method:[Title] ',' [Name] ' . ' [Content] '/ ' [Side_note]")
            return

        embed = discord.Embed(title=title, colour=discord.Colour.red())
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        embed.add_field(name=name, value=content)
        embed.set_footer(text=footer)
        message_ = await channel.send(embed=embed)
        await message_.add_reaction("✅")
        await message_.add_reaction("❌")
        await ctx.message.delete()

    @announce.error
    async def announce_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Correct Method:[Title] ',' [Name] ' . ' [Content] '/ ' [Side_note]")

    # _____________________________________
    # warn
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.client.warnings[guild.id] = {}

    @commands.command()
    @has_permissions(administrator=True)
    async def warn(self, ctx, user: discord.Member, *, msg=None):
        if msg == None:
            msg = "No reason provided."

        em = discord.Embed(title="⚠️• WARNING!! ", description=f"{user.mention} was warned!!",
                           color=discord.Colour.red())
        em.add_field(name="Reason", value=msg)
        em.set_footer(text=f"warning by {ctx.author} ⛔")

        embed = discord.Embed(title="⚠️WARNING!!! ⚠️", description=f"Warning from {ctx.guild.name}")
        embed.add_field(name="Reason", value=msg)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"You were warned by: {ctx.author.name} ", icon_url=ctx.author.avatar_url)

        await user.send(embed=embed)
        await ctx.send(embed=em)

    # _______________________________
    # clear
    @commands.command(aliases=["purge"])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        amount_m = amount + 1
        await ctx.channel.purge(limit=amount_m)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have manage_messages permission')
        else:
            await ctx.send('There was an error while executing the command! Boss has been informed! :red_circle:')
            print(error)

    # _________________________________

    # mute
    @commands.command()
    @has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member):
        role_1 = ctx.guild.get_role(778224719261728809)
        role = ctx.guild.get_role(806192447449333841)
        if ctx.author.guild_permissions.mute_members:
            await user.add_roles(role or role_1)

            em = discord.Embed(colour=discord.Colour.blurple(), timestamp=ctx.message.created_at,
                               title=f"MUTE!! - {user}")
            em.add_field(name="Muted:",
                         value=f"{user.mention} was muted by {ctx.author.mention}...")
            em.set_thumbnail(url=user.avatar_url)
            em.set_footer(text=f"{user} Stay down!")
            await ctx.send(embed=em)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'{ctx.message.author.mention} You do not have the permission to run that command! :red_circle:')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.message.author.mention} There is an Argument missing in that command! :red_circle:\nMute Command Syntax: .mute @user ')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f'{ctx.message.author.mention} To mute someone you need to mention them! :red_circle:\nMute Command Syntax: .mute @user ')
        else:
            await ctx.send(
                'There was an error while executing the command! Boss has been informed! :red_circle:')
            print(error)

    @commands.command()
    @has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        role = ctx.guild.get_role(806192447449333841)
        role_1 = ctx.guild.get_role(778224719261728809)
        if ctx.author.guild_permissions.mute_members:
            await user.remove_roles(role or role_1)
            em = discord.Embed(colour=discord.Colour.green(), timestamp=ctx.message.created_at,
                               title=f"UNMUTE!! - {user}")
            em.add_field(name="UnMuted:",
                         value=f"{user.mention} was unmuted by {ctx.author.mention}...")
            em.set_thumbnail(url=user.avatar_url)
            em.set_footer(text=f"{user} Try to not get muted again!")
            await ctx.send(embed=em)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'{ctx.message.author.mention} You do not have the permission to run that command! :red_circle:')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.message.author.mention} There is an Argument missing in that command! :red_circle:\nMute Command Syntax: .mute @user ')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f'{ctx.message.author.mention} To mute someone you need to mention them! :red_circle:\nMute Command Syntax: .mute @user ')
        else:
            await ctx.send(
                'There was an error while executing the command! Boss has been informed! :red_circle:')
            print(error)

    # _________________________________

    # kick
    @commands.command()
    @has_permissions(manage_roles=True, kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason == None:
            reason = "No reason was given"
        # await ctx.send(f"Banned {member.mention}\n Reason:{reason}")

        embed = discord.Embed(color=discord.Colour.red(), title="❌ KICK CONFORMATION ❌", description=f"Are your sure you want to kick {member.mention}?")
        embed.set_footer(text=f"Kick request by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Reason:", value=reason)
        embed.set_thumbnail(url=member.avatar_url)

        kickbut = await ctx.send(
            embed=embed,
            components=[[
                Button(style=ButtonStyle.red, label="KICK!!", id="kick"),
                Button(style=ButtonStyle.blue, label="Cancel", id="no")]
            ],
        )
        res = await self.client.wait_for("button_click", check=lambda interact: interact.user.id == ctx.author.id and interact.message.id == kickbut.id)
        if res.channel == ctx.channel:
            if res.component.id == "kick":
                await member.kick(reason=reason)
                await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    content=f"{member.mention} has been KICKED!!!"
                )
            elif res.component.id == "no":
                await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    content=f"{member.mention}'s KICK has been CANCELED!!"
                )

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'{ctx.message.author.mention} You do not have the permission to run that command! :red_circle:')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.message.author.mention} There is an Argument missing in that command! :red_circle:\nKick Command Syntax: .kick @user ')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f'{ctx.message.author.mention} To Kick someone you need to mention them! :red_circle:\nKick Command Syntax: .kick @user ')
        else:
            await ctx.send(
                'There was an error while executing the command! Boss has been informed! :red_circle:')
            print(error)

    # ___________________________________

    # ban
    @commands.command()
    @has_permissions(manage_roles=True, ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if reason == None:
            reason = "No reason was given"
        # await ctx.send(f"Banned {member.mention}\n Reason:{reason}")

        embed = discord.Embed(color=discord.Colour.red(), title="⛔ BAN CONFORMATION ⛔", description=f"Are your sure you want to ban {member.mention}?")
        embed.set_footer(text=f"Ban request by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Reason:", value=reason)
        embed.set_thumbnail(url=member.avatar_url)

        banbut = await ctx.send(
            embed=embed,
            components=[[
                Button(style=ButtonStyle.red, label="BAN!!", id="ban"),
                Button(style=ButtonStyle.blue, label="Cancel", id="no")]
            ],
        )
        res = await self.client.wait_for("button_click", check=lambda interact: interact.user.id == ctx.author.id and interact.message.id == banbut.id)
        if res.channel == ctx.channel:
            if res.component.id == "ban":
                await member.ban(reason=reason)
                await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    content=f"{member.mention} has been BANNED!!!"
                )
            elif res.component.id == "no":
                await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    content=f"{member.mention}'s BAN has been CANCELED!!"
                )

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'{ctx.message.author.mention} You do not have the permission to run that command! :red_circle:')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.message.author.mention} There is an Argument missing in that command! :red_circle:\nBan Command Syntax: .ban @user ')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f'{ctx.message.author.mention} To Ban someone you need to mention them! :red_circle:\nBan Command Syntax: .ban @user ')
        else:
            print(error)
            await ctx.send(
                'There was an error while executing the command! Boss has been informed! :red_circle:')

    # unban
    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        if ctx.author.guild_permissions.administrator:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")

            for bans in banned_users:
                user = bans.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f"Unbanned {user.mention}")
                    return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'{ctx.message.author.mention} You do not have the permission to run that command! :red_circle:')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.message.author.mention} There is an Argument missing in that command! :red_circle:\nUnBan Command Syntax: .unban @user ')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f'{ctx.message.author.mention} To mute someone you need to mention them! :red_circle:\nUnBan Command Syntax: .unban @user ')
        else:
            await ctx.send(
                'There was an error while executing the command! Boss has been informed! :red_circle:')
            print(error)

    # temporary delchannel
    # @commands.command(name='delchannel', help='delete a channel with the specified name')
    # async def delete_channel(self, ctx):
    # check if the channel exists
    # name = ctx.channel.name
    # if != "general":
    # existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)

    # if the channel exists
    # if existing_channel is not None:
    # await existing_channel.delete()
    # if the channel does not exist, inform the user
    # else:
    # await ctx.send(f'No channel named, "{channel_name}", was found')

    # __________________________________
    # create channel
    @commands.command()
    @has_permissions(manage_channels=True)
    async def createchannel(self, ctx, *, name):
        names = name.split()
        em = discord.Embed(color=discord.Colour.blue(), title="Create channel")
        em.set_thumbnail(url=ctx.author.avatar_url)
        em.set_footer(text=f"Channels created by {ctx.author.mention}", icon_url=ctx.author.avatar_url)

        for i in names:
            await ctx.guild.create_text_channel(i)
            em.add_field(name="Name:", value=f"`{i}`")

        await ctx.send(embed=em)

    # delete channel
    @commands.command()
    @has_permissions(manage_channels=True)
    async def delchannel(self, ctx, channel: discord.TextChannel):
        await channel.delete()
        em = discord.Embed(color=discord.Colour.purple())
        em.set_thumbnail(url=ctx.author.avatar_url)
        em.add_field(name="Channels deleted", value=f"\n\n`{channel}` was deleted by {ctx.author.name}")

        await ctx.send(embed=em)


# ________________________________________________________

def setup(client):
    client.add_cog(MOD_commands(client))
