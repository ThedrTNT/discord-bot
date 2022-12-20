import discord
import os
from dotenv import load_dotenv
import random
from responses import responses
from discord.ext import commands

load_dotenv()
PUBLIC_KEY = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

description = '''A simple bot'''
bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):    
    if message.author.bot == False and bot.user.mentioned_in(message):
        response = random.choice(responses)
        await message.channel.send(response)
    else:
        await bot.process_commands(message)

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def addresponse(ctx, *, text: str):
    responses.append(text)
    await ctx.send(f'Added new response: {text}')
    print(f'Added new response: {text}')

bot.run(PUBLIC_KEY)