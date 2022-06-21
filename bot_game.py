import discord
from discord.ext import commands
import random 
import asyncio
from typing import List, Tuple

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.initiator = None
        self.initiator_goal = None
        self.initiator_mark = 1
        self.challenger = None
        self.challenger_goal = None
        self.whos_go = None
        self.current_int = 1
        self.board = [[0,0,0], [0,0,0], [0,0,0]]
        self.int2char = {0 : ' ', 1: 'X', 2: 'O'}

    @commands.command(pass_context=True, aliases=['pg'])
    async def play_game(self, ctx, name: str) -> None:
        '''
        Initiate a game of Tic Tac Toe with a user.
        '''
        self.initiator = None
        self.initiator_goal = None
        self.initiator_mark = 1
        self.challenger = None
        self.challenger_goal = None
        self.current_int = 1
        self.board = [[0,0,0], [0,0,0], [0,0,0]]

        self.initiator_goal = random.choice(['win', 'lose', 'draw'])
        self.challenger_goal = random.choice(['win', 'lose', 'draw'])

        self.initiator = ctx.message.author
        for member in ctx.guild.members:
            if member.name.lower() == name.lower():
                self.challenger = member
  
        if self.challenger is None:
            await ctx.send(f'{name} is not in this server.')
            return
        
        await ctx.send(f'{self.initiator.name} has challenged {self.challenger.name} to a game of Tic Tac Toe!')

        try:
            await self.initiator.send(f"You started the game, your goal is to {self.initiator_goal}.")
        except:
            await ctx.send(f'Could not message {self.initiator.name}! Game aborted.')
            await self.reset(ctx)
            return 

        try:
            await self.challenger.send(f"You have been challenged, your goal is to {self.challenger_goal}.")
        except:
            await ctx.send(f'Could not message {self.challenger.name}! Game aborted.')
            await self.reset(ctx)
            return 
        

        self.whos_go = random.choice([self.initiator.name, self.challenger.name])

        if self.whos_go == self.challenger.name:
            self.current_int = 2

        await ctx.send(f'{self.whos_go} goes first.')


    @commands.command(pass_context=True, aliases=['p'])
    async def place(self, ctx, x: int, y: int) -> None:
        if ctx.message.author.name != self.whos_go:
            await ctx.send(f'It is not your turn, {ctx.message.author.name}.')
            return

        if self.board[x][y] != 0:
            await ctx.send(f'{self.whos_go}, please choose an empty cell.')
            return 

        self.board[x][y] = self.current_int

        if self.current_int == 1:
            self.current_int = 2
        else:
            self.current_int = 1

        self.whos_go = self.initiator.name if self.whos_go == self.challenger.name else self.challenger.name

        board_str = self.print_board(self.board)

        await ctx.send(f'{ctx.message.author.name} placed a {self.int2char[self.current_int]} at [{x}, {y}].\n`{board_str}`')

        won, mark = self.is_done(self.board)

        if not won:
            return

        p1score, p2score = False, False

        if won and mark==0:
            if self.initiator_goal == "draw":
                await ctx.send(f'{self.initiator.name} has achieved their goal of a draw!')
                p1score = True
            if self.challenger_goal == "draw":
                await ctx.send(f'{self.challenger.name} has achieved their goal of a draw!')
                p2score = True
        elif won and mark==1:
            if self.initiator_goal == "win":
                await ctx.send(f'{self.initiator.name} has achieved their goal of winning!')
                p1score = True
            if self.challenger_goal == "lose":
                await ctx.send(f'{self.challenger.name} has achieved their goal of losing!')
                p2score = True
        elif won and mark==2:
            if self.initiator_goal == "lose":
                await ctx.send(f'{self.initiator.name} has achieved their goal of losing!')
                p1score = True
            if self.challenger_goal == "win":
                await ctx.send(f'{self.challenger.name} has achieved their goal of winning!')
                p2score = True
        
        if not p1score:
            await ctx.send(f'{self.initiator.name} did not achieve their goal!')
        if not p2score:
            await ctx.send(f'{self.challenger.name} did not achieve their goal!')
        
        await ctx.send(f'Scores:\n {self.initiator.name} : {int(p1score)}\n {self.challenger.name} : {int(p2score)}')
        return 

    def is_won(self, board: List[List[int]]) -> Tuple[bool, int]:
        for row in board:
            if row[0] == row[1] == row[2] and row[0] != 0:
                return True, row[0]
        
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 0:
                return True, board[0][col]
        
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
            return True, board[0][0]

        return False, 0

    @commands.command(pass_context=True, aliases=['r'])
    async def reset(self, ctx) -> None:
        '''
        Initiate a game of Tic Tac Toe with a user.
        '''
        self.initiator = None
        self.initiator_goal = None
        self.initiator_mark = 1
        self.challenger = None
        self.challenger_goal = None
        self.whos_go = None
        self.current_int = 1
        self.board = [[0,0,0], [0,0,0], [0,0,0]]

    def print_board(self, board: List[List[int]]) -> str:
        board_str = "-------------\n"
        for row in board:
            board_str += f"| {self.int2char[row[0]]} | {self.int2char[row[1]]} | {self.int2char[row[2]]} |\n"
            board_str +=  "-------------\n"
        return board_str
    
    def is_done(self, board: List[List[int]]) -> Tuple[bool, int]:
        unq_cells = set()

        won, mark = self.is_won(board)

        if won:
            return won, mark

        for row in board:
            for cell in row:
                unq_cells.add(cell)
        
        if 0 in unq_cells:
            return False, 0
        
        return True, 0