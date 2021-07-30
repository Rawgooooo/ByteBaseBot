import discord
from discord.ext import commands
from main import get_quote
import random
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
import praw
import giphy_client
from giphy_client.rest import ApiException

reddit = praw.Reddit(client_id = "OmwnFHHD7mIlDV0QhTmQ4Q",
                     client_secret = "EE-S5y9OWKOl42oO0cJ6RliCJ5wjmw",
                     username = "FrostingNo3034",
                     password = "r4gutrueno",
                     user_agent = "pythonpraw",
                     check_for_async = False)


# ___________________________________
# ___________________________

class dwellers(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ___________________________________________________________________

    # test
    @commands.command()
    async def bot(self, ctx):
        await ctx.send("You Rang?")

    # ______________________________

    # poll
    @commands.command()
    async def poll(self, ctx, *, msg):
        channel = ctx.channel
        try:
            head = msg.split(",")[0]
            ops = msg.split(",")[1]
            op1, op2 = ops.split(" or")
            txt = f"{head}\n\nReact with:\n✅ for {op1} \nor \n❌ for {op2}"
        except:
            await channel.send("Correct Method:<Title> , <Choice1> or <Choice2>")
            return

        embed = discord.Embed(title="Poll", description=txt, colour=discord.Colour.dark_blue())
        message_ = await channel.send(embed=embed)
        await message_.add_reaction("✅")
        await message_.add_reaction("❌")
        await ctx.message.delete()

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.message.author.mention} There is an Argument missing in that command! :red_circle:\nPoll Command Syntax: [Title] , [Choice1] or [Choice2]')

    # ______________________________

    # hi
    @commands.command(aliases=["hello", "Hi", "Hello"])
    async def hi(self, ctx):
        await ctx.send("Hello" + ", " + ctx.message.author.mention)

    # _____________________________

    # ping
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong {round(self.client.latency * 1000)}ms")

    # _____________________________

    # quotes
    @commands.command()
    async def inspire(self, ctx):
        quote = get_quote()
        await ctx.send(quote)

    # _____________________________
    # roast
    @commands.command()
    async def roast(self, ctx, target: discord.Member=None):
        if target == None:
            target = ctx.message.author
            await ctx.send(f"U want me to roast u DUMBASS {target.mention}? Mention someone BAKA")
        else:
            user = target
            roasts = ["You’re the reason God created the middle finger.",
                      "You’re a grey sprinkle on a rainbow cupcake.",
                      "Better not tell you now.",
                      "If your brain was dynamite, there wouldn't’t be enough to blow your hat off.",
                      "Light travels faster than sound which is why you seemed bright until you spoke.",
                      "Your face makes onions cry.",
                      "You look so pretty. Not at all gross, today.",
                      "If you have a problem with me, write the problem on a piece of paper, fold it, and shove it up your ass.",
                      "I’m busy right now, can I ignore you another time?",
                      "Of course I’m talking like an idiot… how else could you understand me?",
                      "You’re entitled to your incorrect opinion.",
                      "Is your ass jealous of the amount of sh*t that comes out of your mouth?",
                      "You’re the reason this country has to put directions on shampoo.",
                      "You are like a cloud. When you disappear it’s a beautiful day.",
                      "I’m not a nerd, I’m just smarter than you.",
                      ""]
            roast = random.choice(roasts)

        # come_back = ["Not insulting you, I’m describing you."]
            await ctx.send(f"{user.mention} {roast.upper()}")

    # _____________________________

    # toss
    @commands.command()
    async def toss(self, ctx):
        # coin_sides = [r"E:\PC\py\disc_2ctx\heads.png", r"E:\PC\py\disc_2ctx\tails.png"]
        coin_sides = ["Heads", "Tails"]
        coin = random.choice(coin_sides)
        # file = discord.File(coin)
        await ctx.send(coin)

    # _________________________

    # Gayrate
    @commands.command()
    async def gayrate(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        target = user
        percentage = random.randint(0, 100)
        await ctx.send(f"{target.mention} is {percentage}% Gay")

    # _________________________

    # Simprate
    @commands.command()
    async def simprate(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        target = user
        percentage = random.randint(0, 100)
        await ctx.send(f"{target.mention} is {percentage}% Simp")

    # _____________________________
    # reddit memes
    @commands.command(aliases=["MEME", "memes", "MEMES"])
    async def meme(self, ctx, subred = "memes", msg=None):
        subreddit = reddit.subreddit(subred)
        all_subs = []
        top = subreddit.hot(limit=100)

        for submissions in top:
            all_subs.append(submissions)
        random_subs = random.choice(all_subs)

        if msg != None:
            search = subreddit.search(msg)
            name = search.title
            url = search.url
            em = discord.Embed(title=name)
            em.set_image(url = url)
            await ctx.send(embed=em)

        elif msg == None:
            name = random_subs.title
            url = random_subs.url
            em = discord.Embed(title=name)
            em.set_image(url = url)
            await ctx.send(embed=em)

    # ______________________

    # 8ball
    @commands.command(aliases=["8ball", "eightball"])
    async def eight_ball(self, ctx, *, question):
        responses = ["As I see it, yes",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don’t count on it.",
                     "It is certain.",
                     "It is decidedly so.",
                     "Most likely.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Outlook good.",
                     "Reply hazy, try again.",
                     "Signs point to yes.",
                     "Very doubtful.",
                     "Without a doubt.",
                     "Yes.",
                     "Yes – definitely.",
                     "You may rely on it."]
        await ctx.send(f"{ctx.message.author.mention}: {question}\n8Ball    : {random.choice(responses)}")

    @eight_ball.error
    async def ebal_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.message.author.mention} There is an Argument missing in that command! :red_circle:\n8ball Command Syntax: .8ball [query] ')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f'{ctx.message.author.mention} To mute someone you need to mention them! :red_circle:\nBan Command Syntax: .8ball [query] ')
        else:
            await ctx.send(
                'There was an error while executing the command! Boss has been informed! :red_circle:')

    # ______________________________

    # Truth
    @commands.command()
    async def truth(self, ctx):
        responses = ["If you could be invisible, what is the first thing you would do?",
                     "What is a secret you kept from your parents?",
                     "What is the most embarrassing music you listen to?",
                     "What is one thing you wish you could change about yourself?",
                     "Who is your secret crush?",
                     "Who is the last person you creeped on social media?",
                     "If a genie granted you three wishes, what would you ask for?",
                     "What is your biggest regret?",
                     "Where is the weirdest place you've ever gone to the bathroom?",
                     "Read the last thing you sent your best friend or significant other out loud.",
                     "When was the last time you lied? And details",
                     "What's the most embarrassing thing you ever did with your crush",
                     "When was the last time you cried?",
                     "What's your biggest fear?",
                     "What's one silly thing you can't live without?",
                     "What person do you text the most?",
                     "Who is your celebrity crush?",
                     "What is your biggest insecurity?",
                     "How many times a week do you wear the same pants?",
                     "What is your greatest fear in a relationship?",
                     "Do you still have feelings for any of your exes?",
                     "When’s the last time you got dumped?",
                     "What’s the most childish thing you still do?",
                     "When’s the last time you made someone else cry?",
                     "If you could become invisible, what’s the worst thing you’d do?",
                     "What’s one thing in your life you wish you could change?",
                     "What’s the weirdest thing you’ve ever done in a bathroom?",
                     "When’s the last time you got caught in a lie?",
                     "What’s the worst advice someone else has ever given you?",
                     "When did you stop believing in Santa Claus?",
                     "What’s the weirdest thing you’ve ever collected?", ]

        await ctx.send(
            f"The Court: REPEAT AFTER ME!\n\n*I SWEAR BY ALL MEANS\nTHAT THE WORDS I SHALL GIVE\nTO THE AUDIENCE IN THIS TURN\nSHALL BE THE TRUTH\nTHE WHOLE TRUTH\nAND NOTHING BUT THE TRUTH*\n\n Question    : {ctx.message.author.mention} {random.choice(responses)}")

    # ______________________________
    # opinions
    # Truth
    @commands.command(aliases=["opinion", "up"])
    async def unpopular_opinion(self, ctx):
        responses = [
            "You produce carbondioxide every second for plants to make oxygen. Which helps others breath. So if anyone tells u that u r useless.... ITS NOT TRUE. u r useful just by living",
            "As a kid 99.9% of the time we cried is due to physical pain. As adults tho 99.9% of the time we cried is due to emotional pain.",
            "You can't lick your elbow",
            "The words *short* *shorter* and *shortest* are just the long, longer and longest versions of the word 'short'.",
            "We say things are on fire but actually its fire that's blazing on top of things.",
            "Dark is written with a 'k' instead of a 'c', maybe because we can't *see* in the dark.",
            "Your parents always told u 'Don't talk to strangers'. But the only way to make frnds is to talk to strangers. 'Literally'",
            "If u r wearing a sweater and u r sweating, doesn't that make u the sweater",
            "Light of the moon is just the reflection of sun ryt? Then how come vampires don't burn at night?",
            "If u just put a bunch of brains in washing machine. Isn't that also 'literally' considered as brain washing?",
            "Usually you breath and blink on autopilot. Now that I have mentioned u r doing it manually. Most of u",
            "Earth revolves around sun, sun around the centre of our galaxy, our galaxy spiralling with Andromeda moving around something else. Thinking of this.. every second earth is at constant motion to very different spot from the previous one and will never come back to it.",
            "Your age in years is how many times the u went around the sun. In months its how many times the moon went around u.",
            "Maybe v r just characters in a universe sized video game. Or just AI's of some high level aliens.",
            "Religion is HOAX created by stone-age ppl for fun",
            "Peter Parker is a teen with a spider hickey\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t-Aeyen_Jxmil",
            "WINTER fashion better than SUMMER fashion",
            "Brunch is good, But its Dramatically overrated",
            "Mushrooms are fucking disgusting! They are fungus that grows on shit."
            "BTS is Ultra-Pro-Max-Legendary-S-R Overrated",
            "The new generation gives too much emphasis on music/beats and not enough on lyrics. That’s why we have so many mumble rappers. Everyone is like mmm...ummm...aah..hmhmh...wtf u cant even understand words",
            "Chinese food is disgusting",
            "Star Wars is good. But not soo good",
            "99% of school-poetry sucks",
            "Brown Cars",
            "Harry Potter is overrated",
            "Trump was not that bad"]

        await ctx.send(random.choice(responses))

    # ______________________________
    # blank text
    @commands.command(aliases=["ec", "blank"])
    async def empty_txt(self, ctx):
        await ctx.send("You can CopyPasta this anywhere you want\n" "'" + "‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎ " + "'")

    # _____________________________
    # wanted
    @commands.command()
    async def wanted(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        wanted = Image.open("wanted.jpg")
        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((250, 305))
        wanted.paste(pfp, (190, 260))

        wanted.save("profile.jpg")
        await ctx.send(file=discord.File("profile.jpg"))

    # _____________________________
    # slap
    @commands.command()
    async def slap(self, ctx, user: discord.Member = None):

        slap = Image.open("slap.jpg")
        asset1 = user.avatar_url_as(size=128)
        data1 = BytesIO(await asset1.read())
        asset2 = ctx.author.avatar_url_as(size=128)
        data2 = BytesIO(await asset2.read())
        slaper_i = Image.open(data2)
        reciever_i = Image.open(data1)

        slaper = slaper_i.resize((77, 91))
        slap.paste(slaper, (290, 22))
        reciever = reciever_i.resize((169, 192))
        slap.paste(reciever, (15, 10))

        slap.save("slap_done.jpg")
        await ctx.send(file=discord.File("slap_done.jpg"))

    # _______________________________________________________________________
    # RIP
    @commands.command()
    async def rip(self, ctx, user:discord.Member=None):
        if user == None:
            user = ctx.author

        wanted = Image.open("rip-stone.png")
        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((120, 130))
        pfp = pfp.convert("RGBA")
        wanted = wanted.convert("RGBA")

        wanted.paste(pfp, (140, 250))

        wanted.save("rip.png")
        await ctx.send(file=discord.File("rip.png"))

    # _____________________________
    # shitstep
    @commands.command()
    async def shit(self, ctx, msg):
        img = Image.open("shit.jpg")
        f = ImageFont.truetype("Mont-HeavyDEMO.ttf", 50)

        txt = Image.new('L', (1150, 500))
        d = ImageDraw.Draw(txt)

        d.text((0, 0), msg, font=f, fill=255)
        w = txt.rotate(50, expand=1)

        img.paste(ImageOps.colorize(w, (0, 0, 0), (0, 0, 0)), (242, 60), w)
        img.save("shit_edit.jpg")

        await ctx.send(file=discord.File("shit_edit.jpg"))

    # __________________________________
    # translate
    @commands.command()
    async def translate(self, ctx, lang, *msg):
        await ctx.send(" :red_circle: Google Translator has gone haywire for now, so..... try again later!!!")

    # ___________________________
    # giphy
    @commands.command(aliases=["gif", "GIF"])
    async def giphy(self, ctx, *, q="Smile"):
        api_key = "2mAASqBsHCupfewGiRh7Bfa7NNUGYbNZ"
        api_instance = giphy_client.DefaultApi()

        try:
            api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating="pg")
            ls = list(api_response.data)
            gif = random.choice(ls)

            await ctx.send(gif.embed_url)

        except ApiException as e:
            await ctx.send("There was a problem with your input or the Giphy developers. It will be fixed.")


    @giphy.error
    async def giphy_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('No GIFs exist for your search.')
        else:
            await ctx.send(':red_circle: There was a problem with your input or the Giphy developers. It will be fixed.')
            raise error

    
    
# ______________________________________________________________________

def setup(client):
    client.add_cog(dwellers(client))
