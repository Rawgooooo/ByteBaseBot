import discord
from discord.ext import commands

server_c = [{"name":"🛠️ server", "desc":"Get your current server details"},
            {"name":"avatar", "desc":"Look at the avatar of anyone"},
            {"name": "🚪 invite", "desc": "Invite the bot to your server"},
            {"name": "🚪 createinvite", "desc": "create this server's invite link"},
            {"name": "💡 bytebaseinvite", "desc": "Join our server"},
            {"name": "prefix", "desc": "Change my prefix for this server"},
            {"name": "serverdecorators", "desc": "Decorate your server with these!!"},
            {"name":"👨 whois", "desc":"Get profile details of the person you mention"}]

Mod_c = [{"name":"addrole", "desc":"Grants a person the role"},
         {"name":"delrole", "desc":"removes role from the person"},
         {"name":"📢 announce", "desc":"Announce something"},
         {"name":"⚠ Warn", "desc":"Warn a user!"},
         {"name":"🚫 ban", "desc":"Ban anyone"},
         {"name":"kick", "desc":"kick anyone from the server"},
         {"name":"🔇 mute", "desc":"Mute a person"},
         {"name":"createchannel", "desc":"create new channel."},
         {"name":"reactrole", "desc":"Create an instant react role message"},
         {"name":"✔ unban", "desc":"Unban a person"}]

common_c = [{"name": "🤖 bot", "desc": "Call the bot"},
            {"name": "👋 hi", "desc": "Say hello to the bot"},
            {"name": "❗ ping", "desc": "Check ping"},
            {"name": ":8ball: 8ball", "desc": "Ask the 8ball"},
            {"name": "empty text", "desc": "Get an empty text"},
            {"name": "🏳️‍🌈 gayrate", "desc": "Check how much of a gay someone is"},
            {"name": "🏳️‍🌈 simprate", "desc": "Check how much of a simp someone is"},
            {"name": "inspire", "desc": "Get some motivational quotes"},
            {"name": ":x: poll :white_check_mark:️", "desc": "Create an instant simple poll"},
            {"name": "roast", "desc": "Roast a friend of yours"},
            {"name": "🪙 toss", "desc": "Toss a coin"},
            {"name": "giphy", "desc":"send a giphy"},
            {"name": "🤪 meme", "desc": "Get a meme from r/memes"},
            {"name": "truth", "desc": "Ask truth questions"},
            {"name": "translate", "desc": "language translate"},
            {"name": "⚰ rip", "desc": "Rip image for a person"},
            {"name": "wanted", "desc": "Make a wanted poster"},
            {"name": "shit", "desc": "Step on shit meme"},
            {"name": "opinion", "desc": "Get some unpopular opinions"}]


Economy_c = [{"name": "💰 balance", "desc":"Check your money balance"},
             {"name": "🥺 beg", "desc": "Beg for money"},
             {"name": "🏬 buy", "desc": "Buy items from store"},
             {"name": "💰 deposit", "desc": "Deposit some cash in bank"},
             {"name": "🏧 withdraw", "desc": "Withdraw cash from bank"},
             {"name": "🕵️ rob", "desc": "Rob a person"},
             {"name": "🏬 shop", "desc": "Visit the store"},
             {"name": "💸 transfer", "desc": "Transfer money to someone"},
             {"name": "🔐 vault", "desc": "Check your inventory"},
             {"name": "₿ cryptocurrency", "desc": "Check crypto currency prices!"},
             {"name": "🔒 status", "desc": "Active Passive stop ROB"}]

Games_c = [{"name": "⭕ tictactoe :x:", "desc": "Play the famous XO"}]

VC_c = [{"name": "📞 join", "desc": "Join VC"},
        {"name": "⛔ leave", "desc": "Leave VC"}]

math = [{"name":"+ • add", "desc":"Add multiple numbers"},
         {"name":"- • minus", "desc":"Subtract 2 numbers"},
         {"name":"❌ • multiply", "desc":"Multiply 2 numbers"},
         {"name":"% • divide", "desc":"Get quotient and remainder after division"},
         {"name":"X² • square", "desc":"Square a number"},
         {"name":"√ • sqaureroot", "desc":"Get the square root of a number"},
         {"name":"^ • power", "desc":"Raise a number to 'multiple' times."},
         {"name":"❗ • factorial", "desc":"Get the factorial of a number"}]

Help = [{"name": "🛠️  • UTILS • 1", "desc": "Server detail commands"},
        {"name": "👮 ‍• MODS • 2", "desc": "All mod commands"},
        {"name": "😎 • FUN • 3", "desc": "Common commands"},
        {"name": "💰 • MONEY • 4", "desc": "Financial commands"},
        {"name": "🎮 • GAMES • 5", "desc": "Game commands"},
        {"name": "📞 • VC • 6", "desc": "VC commands"},
        {"name": "📏📐🗄 • Math • 7", "desc": "Do math problems"},
        {"name": "•HELP•", "desc": "Use help <page_number> to view all commands from a category"}]

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command("help")

# ______________________________________________________________________

    @commands.command()
    async def help(self, ctx, page=0):

        if page == 0:
            em0 = discord.Embed(title="**COMMANDS HELP**", color=discord.Colour.random())
            em0.set_thumbnail(url=self.client.user.avatar_url)
            for item in Help:
                name = item["name"]
                desc = item["desc"]
                em0.add_field(name=name, value=desc)
            await ctx.send(embed=em0)

        elif page == 1:
            em1 = discord.Embed(title="**COMMANDS HELP** • UTILITIES", color=discord.Colour.random())
            em1.set_thumbnail(url=self.client.user.avatar_url)
            em1.set_footer(text="For further help do .help <command name> ", icon_url=self.client.user.avatar_url)
            for item in server_c:
                name = item["name"]
                desc = item["desc"]
                em1.add_field(name=name, value=desc)
            await ctx.send(embed=em1)

        elif page == 2:
            em2 = discord.Embed(title="**COMMANDS HELP** • MANAGEMENT", color=discord.Colour.random())
            em2.set_thumbnail(url=self.client.user.avatar_url)
            em2.set_footer(text="For further help do .help <command name> ", icon_url=self.client.user.avatar_url)
            for item in Mod_c:
                name = item["name"]
                desc = item["desc"]
                em2.add_field(name=name, value=desc)
            await ctx.send(embed=em2)

        elif page == 3:
            em3 = discord.Embed(title="**COMMANDS HELP** • FUN", color=discord.Colour.random())
            em3.set_thumbnail(url=self.client.user.avatar_url)
            em3.set_footer(text="For further help do .help <command name> ", icon_url=self.client.user.avatar_url)
            for item in common_c:
                name = item["name"]
                desc = item["desc"]
                em3.add_field(name=name, value=desc)
            await ctx.send(embed=em3)

        elif page == 4:
            em4 = discord.Embed(title="**COMMANDS HELP** • ECONOMY", color=discord.Colour.random())
            em4.set_thumbnail(url=self.client.user.avatar_url)
            em4.set_footer(text="For further help do .help <command name> ", icon_url=self.client.user.avatar_url)
            for item in Economy_c:
                name = item["name"]
                desc = item["desc"]
                em4.add_field(name=name, value=desc)
            await ctx.send(embed=em4)

        elif page == 5:
            em5 = discord.Embed(title="**COMMANDS HELP** • GAMES", color=discord.Colour.random())
            em5.set_thumbnail(url=self.client.user.avatar_url)
            em5.set_footer(text="For further help do .help <command name> ", icon_url=self.client.user.avatar_url)
            for item in Games_c:
                name = item["name"]
                desc = item["desc"]
                em5.add_field(name=name, value=desc, inline=False)
            await ctx.send(embed=em5)

        elif page == 6:
            em6 = discord.Embed(title="**COMMANDS HELP** • VC", color=discord.Colour.random())
            em6.set_thumbnail(url=self.client.user.avatar_url)
            em6.set_footer(text="For further help do .help <command name> ", icon_url=self.client.user.avatar_url)
            for item in VC_c:
                name = item["name"]
                desc = item["desc"]
                em6.add_field(name=name, value=desc, inline=False)
            await ctx.send(embed=em6)

        elif page == 7:
            em6 = discord.Embed(title="**COMMANDS HELP** • MATH", color=discord.Colour.random())
            em6.set_thumbnail(url=self.client.user.avatar_url)
            em6.set_footer(text="For further help do .help <command name> ", icon_url=self.client.user.avatar_url)
            for item in math:
                name = item["name"]
                desc = item["desc"]
                em6.add_field(name=name, value=desc)
            await ctx.send(embed=em6)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Pls use page numbers to navigate through help commands")



# ______________________________________________________________________

def setup(client):
    client.add_cog(help(client))
