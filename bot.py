import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# import files with cogs
import bot_game

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

# load token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$', case_insensitive=True, intents=intents)


# make way for custom help command
bot.remove_command('help')
# custom help command
@bot.command(pass_context=True, aliases=['h'])
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    embed.set_author(name='help')
    embed.add_field(name='!play_game, alias=[!pg]', 
                    value='Challenge someone to a game of Tic Tac Toe with incomplete information. You must specify a user.',
                    inline=False)
    embed.add_field(name='!place, alias=[!p]', 
                value='Places a mark on the board at the specified x y coordinates.',
                inline=False)
    await ctx.send(embed=embed)

# notify that bot is running
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# add misc commands cog
bot.add_cog(bot_game.BotCommands(bot))

# run the bot
bot.run(TOKEN)
