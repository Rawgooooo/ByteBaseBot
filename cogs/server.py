import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json, contextlib, io


class server(commands.Cog):
    def __init__(self, client):
        self.client = client
# _______________________________________

    @commands.command(help="Get server details")
    async def server(self, ctx):
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
        owner = self.client.get_user(int(ctx.guild.owner.id))
        region = str(ctx.guild.region)

        embed2 = discord.Embed(timestamp=ctx.message.created_at, color=ctx.author.color)
        embed2.add_field(name='Name', value=f"{ctx.guild.name}")
        embed2.add_field(name='Owner', value=owner)
        embed2.add_field(name='Verification Level', value=str(ctx.guild.verification_level), inline=False)
        embed2.add_field(name="Region:", value=region.title(), inline=False)
        embed2.add_field(name='Highest role', value=ctx.guild.roles[-1])
        embed2.add_field(name='Number of roles', value=str(role_count))
        embed2.add_field(name='Contributors:', value="None", inline=False)
        embed2.add_field(name='Number Of Members', value=ctx.guild.member_count)
        embed2.add_field(name='Bots:', value=(', '.join(list_of_bots)))
        embed2.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'),
                         inline=False)
        embed2.set_thumbnail(url=ctx.guild.icon_url)
        embed2.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed2.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)

        await ctx.send(embed=embed2)

    # ________________________

    # _________________________

    # avatar
    @commands.command(help="See avatar of someone", aliases=["av", "dp", "pfp"])
    async def avatar(self, ctx, *, avamember: discord.Member = None):
        if avamember == None:
            avamember = ctx.message.author
        else:
            pass
        userAvatarUrl = avamember.avatar_url
        embed = discord.Embed(description=f"Avatar of {avamember}", color=discord.Colour.blue())
        embed.set_author(name=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=userAvatarUrl)
        await ctx.send(embed=embed)

    # _________________________

    # whois
    @commands.command(help="Check who is who", aliases=["who", "profile"])
    async def whois(self, ctx, *, member: discord.Member = None):
        if not member:  # if member is no mentioned
            member = ctx.message.author  # set member as the author

        roles = [role for role in member.roles]
        embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                              title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Server Nick:", value=member.display_name)
        embed.add_field(name="Status", value=member.status)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="Roles:", value="".join([role.mention for role in roles]), inline=False)
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.send(embed=embed)

    # _________________________________
    # official server invite
    @commands.command(aliases=["bbi", "BBI", "bbinvite", "BBINVITE"])
    async def bytebaseinvite(self, ctx):
        await ctx.send("Join the Official Programming server, where I was developed!!! \nhttps://discord.gg/RweEFh7WeU")

    # _________________________________
    # current server invite
    @commands.command(aliases=["ci", "CI", "cinvite", "Cinvite"])
    async def createinvite(self, ctx):
        link = await ctx.channel.create_invite(max_age=42000, unique=False)
        await ctx.send(f"Here is an instant invite to your server: {link}")

    # ___________________________________
    # invite
    @commands.command(aliases=["i"])
    async def invite(self, ctx):
        await ctx.send("Invite me to your server so that you can enjoy my presence over there too!!\nhttps://discord.com/api/oauth2/authorize?client_id=797168260419813396&permissions=8&scope=bot")

    # ______________________
    # change prefix
    @commands.command(aliases=["cp", "prefix", "PREFIX", "CP"])
    async def changeprefix(self, ctx, prefix):

        with open("prefix.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefix.json", "w") as f:
            json.dump(prefixes, f, indent=3)

        await ctx.send(f"My prefix for this server has been updated to: {prefix}")

    @changeprefix.error
    async def cp_error(self, ctx, error):
        with open("prefix.json", "r") as f:
            prefixes = json.load(f)
        pre = prefixes[str(ctx.guild.id)]

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Enter your new prefix:red_circle: \nCorrect syntax: {pre}cp <your new prefix>")

    # ________________________
    # decorator
    @commands.command(aliases=["dec", "decorate", "decorators", "symbols"])
    async def serverdecorators(self, ctx):
        embed = discord.Embed(colour=discord.Colour.dark_theme(), title=f"Server Decorators!!")
        embed.set_footer(text=f"Use these effectively to decorate your server.")

        embed.add_field(name="DASH", value="▬")
        embed.add_field(name="BULLET", value="•")
        embed.add_field(name="‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎ ", value="‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎ ", inline=False)

        embed.add_field(name="LOWER CURVE", value="╰﹕")
        embed.add_field(name="UPPER CURVE", value="╭﹕")
        embed.add_field(name="‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎ ", value="‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎ ", inline=False)

        embed.add_field(name="OPEN MARGIN", value="『")
        embed.add_field(name="CLOSE MARGIN", value="』")
        embed.add_field(name="‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎ ", value="‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎ ", inline=False)

        embed.add_field(name="RIGHT ARROW", value="》")
        embed.add_field(name="LINE", value="┊")

        await ctx.send(embed=embed)

    # _________________________
    # run CODE
    @commands.command()
    async def run(self, ctx, *, code):
        str_obj = io.StringIO()  # Retrieves a stream of data
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        except Exception as e:
            return await ctx.send(f"```{e.__class__.__name__}: {e}```")

        await ctx.send(f'```{str_obj.getvalue()}```')


# ______________________________________________________________________

def setup(client):
    client.add_cog(server(client))
