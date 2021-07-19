import discord
from discord.ext import commands
import json
import math


class maths(commands.Cog):
    def __init__(self, client):
        self.client = client
    # __________________________________________

    # add
    @commands.command(aliases=["ADD", "+"])
    async def add(self, ctx, *, nums):
        a = list(map(int, nums.split()))

        em = discord.Embed(title="Addition", description="Add numbers.", color=discord.Colour.blue())
        em.set_footer(text=f"requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        # for i in a:
        em.add_field(name="Input", value=f"```{a}```")
        em.add_field(name="Sum", value=f"```{math.fsum(a)}```", inline=False)
        await ctx.send(embed=em)

    # __________________________
    # sub
    @commands.command(aliases=["minus", "SUB", "MINUS", "-"])
    async def sub(self, ctx, *, nums):
        a = int(nums.split()[0])
        b = int(nums.split()[1])

        em = discord.Embed(title="Subtraction", description="Subtract two numbers.", color=discord.Colour.green())
        em.set_footer(text=f"requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        em.add_field(name="Input", value=f"```{a} - {b}```")
        em.add_field(name="Difference", value=f"```{a-b}```", inline=False)
        await ctx.send(embed=em)

    # multiply
    @commands.command(aliases=["PROD", "prod", "MULTIPLY", "x", "X", "*"])
    async def multiply(self, ctx, *, nums):
        a = int(nums.split()[0])
        b = int(nums.split()[1])

        em = discord.Embed(title="Multiplication", description="Multiply two numbers.", color=discord.Colour.greyple())
        em.set_footer(text=f"requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        em.add_field(name="Input", value=f"```{a} x {b}```")
        em.add_field(name="Product", value=f"```{a*b}```", inline=False)
        await ctx.send(embed=em)

    # divide
    @commands.command(aliases=["DIV", "div", "DIVIDE"])
    async def divide(self, ctx, *, nums):
        a = int(nums.split()[0])
        b = int(nums.split()[1])

        em = discord.Embed(title="Division", description="Divide two numbers.", color=discord.Colour.purple())
        em.set_footer(text=f"requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        em.add_field(name="Input", value=f"```{a} / {b}```")
        em.add_field(name="Quotient", value=f"```{a/b}```", inline=False)
        em.add_field(name="Remainder", value=f"```{a%b}```")
        await ctx.send(embed=em)

    # square
    @commands.command(aliases=["sq", "SQUARE", "SQ"])
    async def square(self, ctx, nums):
        nums = int(nums)

        em = discord.Embed(title="Square", description="Square of a number.", color=discord.Colour.gold())
        em.set_footer(text=f"requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        em.add_field(name="Input", value=f"```{nums}²```")
        em.add_field(name="Square", value=f"```{nums*nums}```", inline=False)
        await ctx.send(embed=em)

    # square root
    @commands.command(aliases=["SQRT"])
    async def sqrt(self, ctx, nums):
        nums = int(nums)

        em = discord.Embed(title="Square Root", description="Square root of a number.", color=discord.Colour.dark_gold())
        em.set_footer(text=f"requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        em.add_field(name="Input", value=f"```√{nums}```")
        em.add_field(name="Square Root", value=f"```{math.sqrt(nums)}```", inline=False)
        await ctx.send(embed=em)

    # exponents
    @commands.command(aliases=["raise", "POWER", "RAISE", "^"])
    async def power(self, ctx, *, nums):
        a = int(nums.split()[0])
        b = int(nums.split()[1])

        em = discord.Embed(title="Power", description="Exponents", color=discord.Colour.dark_teal())
        em.set_footer(text=f"requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        em.add_field(name="Input", value=f"```{a}^{b}```")
        em.add_field(name="Answer", value=f"```{a**b}```", inline=False)
        await ctx.send(embed=em)

    # factorial
    @commands.command(aliases=["FACTORIAL", "!"])
    async def factorial(self, ctx, nums):
        nums = int(nums)

        em = discord.Embed(title="Factorial", description="Factorial of a number.", color=discord.Colour.magenta())
        em.set_footer(text=f"requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        em.add_field(name="Input", value=f"```!{nums}```")
        em.add_field(name="Factorial", value=f"```{math.factorial(nums)}```", inline=False)
        await ctx.send(embed=em)


# ______________________________________________________________________

def setup(client):
    client.add_cog(maths(client))