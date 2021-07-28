import discord
from discord.ext import commands
from discord_components import *
from asyncio import TimeoutError
import random
from akinator.async_aki import Akinator

# ____________________________________________________________________________

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    # _________________________________________________________________
    # tic tac toe
    player1 = ""
    player2 = ""
    turn = ""
    gameOver = True

    board = []

    winningConditions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    @commands.command(help="Play TicTacToe", aliases=["ttt"])
    async def tictactoe(self, ctx, player_1: discord.Member, player_2: discord.Member = None):
        global count
        global player1
        global player2
        global turn
        global gameOver
        gameOver = True

        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            if player_2 is None:
                player_2 = ctx.author
                pass

            player1 = player_1
            player2 = player_2

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
            elif num == 2:
                turn = player2
                await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
        else:
            await ctx.send("A game is already in progress! Finish it before starting a new one.")

    @commands.command(help="Place your marker for TicTacToe", aliases=["keep", "position", "p"])
    async def place(self, ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        winningConditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    self.checkWinner(winningConditions, mark)
                    print(count)
                    if gameOver:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
            else:
                await ctx.send("It is not your turn.")
        else:
            await ctx.send("Please start a new game using the .tictactoe command.")

    def checkWinner(self, winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                gameOver = True

    @commands.command(help="End Game")
    async def end(self, ctx):
        global gameOver
        gameOver = True
        await ctx.send("game ended")

    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 2 players for this command.\nCorrect format: .tictactoe <Player1> <Player2>")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Please make sure to mention/ping players (ie. {ctx.author.mention}).")

    @place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark. Correct Syntax: p1/2/3/4/5/6/7/8/9")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")

    # _____________________
    # akinator
    @commands.command(name="akinator", aliases=["aki"])
    async def akinator_game(self, ctx):
        aki = Akinator()
        first = await ctx.send("Processing...")
        q = await aki.start_game()

        game_embed = discord.Embed(title=f"{str(ctx.author.name)}'s game of Akinator", description=q,
                                   url=r"https://en.akinator.com/", color=discord.Color.blurple())
        game_embed.set_footer(text=f"Wait for the bot to add reactions before you give your response.")

        option_map = {'✅': 'y', '❌': 'n', '🤷‍♂️': 'p', '😕': 'pn', '⁉️': 'i'}
        """You can pick any emojis for the responses, I just chose what seemed to make sense.
          '✅' -> YES, '❌'-> NO, '🤷‍♂️'-> PROBABLY YES, '😕'-> PROBABLY NO, '⁉️'->IDK, '😔'-> force end game, '◀️'-> previous question"""

        def option_check(reaction, user):  # a check function which takes the user's response
            return user == ctx.author and reaction.emoji in ['◀️', '✅', '❌', '🤷‍♂️', '😕', '⁉️', '😔']

        count = 0
        while aki.progression <= 80:  # this is aki's certainty level on an answer, per say. 80 seems to be a good number.
            if count == 0:
                await first.delete()  # deleting the message which said "Processing.."
                count += 1

            game_message = await ctx.send(embed=game_embed)

            for emoji in ['◀️', '✅', '❌', '🤷‍♂️', '😕', '⁉️', '😔']:
                await game_message.add_reaction(emoji)

            option, _ = await self.client.wait_for('reaction_add', check=option_check)  # taking user's response
            if option.emoji == '😔':  # there might be a better way to be doing this, but this seemed the simplest.
                return await ctx.send("Game ended.")
            async with ctx.channel.typing():
                if option.emoji == '◀️':  # to go back to previous question
                    try:
                        q = await aki.back()
                    except:  # excepting trying-to-go-beyond-first-question error
                        pass
                    # editing embed for next question
                    game_embed = discord.Embed(title=f"{str(ctx.author.nick)}'s game of Akinator", description=q,
                                               url=r"https://en.akinator.com/", color=discord.Color.blurple())
                    continue
                else:
                    q = await aki.answer(option_map[option.emoji])
                    # editing embed for next question
                    game_embed = discord.Embed(title=f"{str(ctx.author.nick)}'s game of Akinator", description=q,
                                               url=r"https://en.akinator.com/", color=discord.Color.blurple())
                    continue

        await aki.win()

        result_embed = discord.Embed(title="My guess....", colour=discord.Color.dark_blue())
        result_embed.add_field(name=f"My first guess is **{aki.first_guess['name']}**",
                               value=aki.first_guess['description'], inline=False)
        result_embed.set_footer(text="Was I right? Add the reaction accordingly.")
        result_embed.set_image(url=aki.first_guess['absolute_picture_path'])
        result_message = await ctx.send(embed=result_embed)
        for emoji in ['✅', '❌']:
            await result_message.add_reaction(emoji)

        option, _ = await self.client.wait_for('reaction_add', check=option_check, timeout=15)
        if option.emoji == '✅':
            final_embed = discord.Embed(title="I'm a genius", color=discord.Color.green())
        elif option.emoji == '❌':
            final_embed = discord.Embed(title="Oof", description="Maybe try again?", color=discord.Color.red())
            # this does not restart/continue a game from where it was left off, but you can program that in if you like.

            return await ctx.send(embed=final_embed)


# ______________________________________________________________________
def setup(client):
    client.add_cog(Games(client))
