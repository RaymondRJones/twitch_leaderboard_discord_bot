import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load the .env file
load_dotenv()

# Read the bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# Run the bot
bot.run(BOT_TOKEN)
