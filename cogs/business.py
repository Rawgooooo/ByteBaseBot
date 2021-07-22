import discord
from discord.ext import commands
import random
import json
import os
from yahoo_fin import stock_info as si

# ____________________________
# economy funcs
# shop items
shopitems_show = [{"name": "⌚ Watch", "price": 1000, "description": "time"},
                  {"name": "📱 Mobile", "price": 5000, "description": "mobile device"},
                  {"name": "💻 Laptop", "price": 8000, "description": "Work"},
                  {"name": "🔒 Lock", "price": 10000, "description": "prevent rob without passive (1 time use)"},
                  {"name": "🔑 MasterKey", "price": 16000, "description": "Open any lock (1 time use)"}]

shopitems = [{"name": "Watch", "price": 1000, "description": "time"},
             {"name": "Mobile", "price": 5000, "description": "mobile device"},
             {"name": "Laptop", "price": 8000, "description": "Work"},
             {"name": "Lock", "price": 10000, "description": "prevent rob without passive (1 time use)"},
             {"name": "MasterKey", "price": 16000, "description": "Open any lock (1 time use)"}]


# bank info
async def get_bank_data():
    with open("eco.json", "r") as f:
        users = json.load(f)
    return users


# account create
async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 5000
        users[str(user.id)]["Status"] = "yes"

    with open("eco.json", "w") as f:
        json.dump(users, f, indent=4)
    return True


# bank update
async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change

    with open("eco.json", "w") as f:
        json.dump(users, f, indent=4)
    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


# buy_this
async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in shopitems:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = int(item["price"])
            break
    if name_ == None:
        return [False, 1]
    cost = price * amount
    users = await get_bank_data()
    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]
    with open("eco.json", "w") as f:
        json.dump(users, f, indent=4)

    await update_bank(user, cost * -1, "wallet")
    return [True, "Worked"]


# sell_this
async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in shopitems:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = item["price"]
            break

    if name_ == None:
        return [False, 1]
    cost = price * amount
    users = await get_bank_data()
    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("eco.json", "w") as f:
        json.dump(user.id, f, indent=4)

    await update_bank(user, cost, "wallet")
    return [True, "Worked"]


# set
async def setap(user, ap):
    users = await get_bank_data()

    if ap == "active":
        users[str(user.id)]["Status"] = "yes"
        with open("eco.json", "w") as f:
            json.dump(users, f, indent=4)
            return
    if ap == "passive":
        users[str(user.id)]["Status"] = "no"
        with open("eco.json", "w") as f:
            json.dump(users, f, indent=4)
            return
    # await update_bank(user, 0, "wallet")


# __________________________________________________________________

class business(commands.Cog):
    def __init__(self, client):
        self.client = client

    # economy
    # _______________________________________
    # balance

    @commands.command(aliases=["bal", "BAL"])
    async def balance(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        else:
            pass
        await open_account(member)
        user = member
        users = await get_bank_data()

        waller_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        embed = discord.Embed(title=f"{member}'s balance", color=member.color)
        embed.add_field(name="Wallet", value=waller_amt)
        embed.add_field(name="Bank", value=bank_amt)
        await ctx.send(embed=embed)

    # ___________________________
    # beg

    @commands.command(aliases=["BEG"])
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    async def beg(self, ctx):
        lenders = ["Billie Eyelash", "Rick Asstley", "Thanos", "Elizabath", "Aeyen Gmail",
                   "Sundar Beger", "Dank memer", "Ronaldo", "Naruto", "Kakuzo", "RDJ",
                   "Trevor Noah", "Selena Gomz", "Ryan Murphy", "Anonymous", "Mr.X", "RaguBagu",
                   "A random person", "Clyde", "Zeus", "saravana stores"]

        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author

        earning = random.randint(0, 201)

        await ctx.send(f"{random.choice(lenders)} pitied you with {earning} coins!!")

        users[str(user.id)]["wallet"] += earning
        with open("eco.json", "w") as f:
            json.dump(users, f, indent=4)

    # beg error
    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('You are on %.2fs cooldown' % error.retry_after)
        raise error

    # ___________________________
    # withdraw

    @commands.command(aliases=["with", "WITH"])
    async def withdraw(self, ctx, amount=100):
        await open_account(ctx.author)
        bal = await update_bank(ctx.author)
        amount = int(amount)

        if amount > bal[1]:
            await ctx.send("you don't have that much money dumbo!")
            return
        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "bank")
        await ctx.send(f"You withdrew {amount} coins")

    # ___________________________
    # deposit

    @commands.command(aliases=["dep", "DEP"])
    async def deposit(self, ctx, amount=100):
        await open_account(ctx.author)
        wallet = await update_bank(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        if amount > wallet[0]:
            await ctx.send("you don't have that much money dumbo!")
            return
        await update_bank(ctx.author, -1 * amount)
        await update_bank(ctx.author, amount, "bank")
        await ctx.send(f"You deposited {amount} coins")

    # ______________________
    # transfer

    @commands.command(aliases=["send", "SEND"])
    async def transfer(self, ctx, member: discord.Member, amount=100):
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank(ctx.author)
        amount = int(amount)

        if amount > bal[1]:
            await ctx.send("you don't have that much money dumbo!")
            return
        await update_bank(ctx.author, -1 * amount, "bank")
        await update_bank(member, amount, "bank")
        await ctx.send(f"{ctx.author.mention} transferred {amount} coins to {member.mention}")

    # ______________________
    # rob

    @commands.command(aliases=["steal", "STEAL", "ROB"])
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member):
        await open_account(member)
        await open_account(ctx.author)
        users = await get_bank_data()
        stats = users[str(member.id)]["Status"]
        # items = users[str(user.id)]["bag"]["item"]

        # for i in items:
        # global item
        # item = []
        # item.append(i)
        # print(item)

        # if "lock" in item:

        # item = [i["item"] for i in users[str(user.id)]["bag"]]
        # if "lock" in item:
        # await ctx.send(f"{member.mention}'s wallet is locked!!")

        # else:
        if stats == "no":
            await ctx.send("Leave the Goodies alone. BAKA!! BAKA!! BAAAAAAA!!!")


        else:
            bal_auth = await update_bank(ctx.author)
            bal = await update_bank(member)
            if bal[0] < 0:
                await ctx.send(f"{member.mention} has no money in wallet")
                return

            amount = random.randint(0, bal[0])
            amount = int(amount)

            await update_bank(member, -1 * amount)
            await update_bank(ctx.author, amount)
            await ctx.send(f"{ctx.author.mention} just robbed {amount} coins from {member.mention}")

    # rob error
    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('You are on %.2fs cooldown' % error.retry_after)

    # active passive
    @commands.command(aliases=["SET"])
    @commands.cooldown(rate=1, per=43200, type=commands.BucketType.user)
    async def set(self, ctx, value):
        await open_account(ctx.author)
        if value.lower() == "active":
            await ctx.send("Your financial status was set as active")
            await setap(ctx.author, value)
            return
        if value.lower() == "passive":
            await ctx.send("Your financial status was set as passive")
            await setap(ctx.author, value)
            return
        # raise error

    # rob error
    @set.error
    async def set_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('You are on %.2fs cooldown' % error.retry_after)

    # ___________________________
    # shop
    @commands.command(aliases=["SHOP", "store", "STORE"])
    async def shop(self, ctx):
        em = discord.Embed(title="Shop")
        for item in shopitems_show:
            name = item["name"]
            price = item["price"]
            description = item["description"]
            em.add_field(name=name, value=f"${price} | {description}", inline=False)

        await ctx.send(embed=em)

    # ___________________________
    # buy
    @commands.command(aliases=["BUY"])
    async def buy(self, ctx, item, amount=1):
        await open_account(ctx.author)
        res = await buy_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("That Object doesnt exist!")
                return
            if res[1] == 2:
                await ctx.send(f"You don't have enough creds in your wallet")
                return

        await ctx.send(f"You just bought {amount} {item} !")

    # sell
    @commands.command()
    async def sell(self, ctx, item, amount=1):
        await open_account(ctx.author)
        res = await sell_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("No such object exists")
                return
            if res[1] == 2:
                await ctx.send(f"You don't have {amount} {item}s in your vault!")
                return
            if res[1] == 3:
                await ctx.send(f"You don't own {item}!")
                return

        await ctx.send(f"You just sold {amount} {item}s!!")

    # ___________________________
    # vault
    @commands.command(aliases=["inv", "INV", "VAULT"])
    async def vault(self, ctx, member: discord.Member = None):

        if member == None:
            member = ctx.author

        await open_account(ctx.author)
        user = member
        users = await get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em = discord.Embed(title="Vault:")
        for item in bag:
            name = item["item"]
            amount = item["amount"]
            em.add_field(name=name, value=amount, inline=False)

        await ctx.send(embed=em)

    # ___________________________
    # leaderboard
    @commands.command(aliases=["lb", "LB"])
    async def leaderboard(self, ctx, x=3):
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total, reverse=True)

        em = discord.Embed(title=f"Top {x} brass' in {ctx.guild.name}",
                           description="This is decided on the basis of the total money a person owns.")
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            mem = self.client.get_user(id_)
            name = mem.name
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == x:
                break
            else:
                index += 1

        await ctx.send(embed=em)

    # _____________________________________
    # _____________________________________
    # crypto currency
    @commands.command(aliases=["cc", "CC", "crypto"])
    async def cryptocurrency(self, ctx):
        cc = si.get_top_crypto()
        em = discord.Embed(title="Crypto Currency", description="get prices of crypto currencies")
        em.add_field(name="Details", value=cc)
        await ctx.send(embed=em)

    # _____________________________________
    # _____________________________________
    # yt API
    '''
    from googleapiclient.discovery import build

    api_key = "AIzaSyDug0kUHm2Sq9QIyJqCs9bPTg-4WUyO-XU"

    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.channels().list(
        part="statistics",
        # forUsername="Byte_Base"
        id="UCGeiFuZeOU-PBiaa3bt6lGQ"
    )

    response = request.execute()
    print(response)'''


# ______________________________________________________________________________________________

def setup(client):
    client.add_cog(business(client))
