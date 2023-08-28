import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
import json

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

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def joke(ctx):
    # Make a GET request to the JokeAPI
    response = requests.get("https://v2.jokeapi.dev/joke/Programming")
    
    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        joke_data = json.loads(response.text)
        
        # Ensure there's no error in the response
        if not joke_data.get("error"):
            # If it's a 'single' type joke, i.e., a one-liner
            if joke_data["type"] == "single":
                await ctx.send(joke_data["joke"])
            # If it's a two-part joke with a setup and a delivery
            elif joke_data["type"] == "twopart":
                await ctx.send(f"{joke_data['setup']}\n{joke_data['delivery']}")
            else:
                await ctx.send("Couldn't fetch a joke at the moment.")
        else:
            await ctx.send("Couldn't fetch a joke at the moment.")
    else:
        await ctx.send("Couldn't fetch a joke at the moment.")

@bot.command()
async def dark(ctx):
    # Make a GET request to the JokeAPI for Dark jokes
    response = requests.get("https://v2.jokeapi.dev/joke/Dark")
    
    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        joke_data = json.loads(response.text)
        
        # Ensure there's no error in the response
        if not joke_data.get("error"):
            # If it's a 'single' type joke, i.e., a one-liner
            if joke_data["type"] == "single":
                await ctx.send(joke_data["joke"])
            # If it's a two-part joke with a setup and a delivery
            elif joke_data["type"] == "twopart":
                await ctx.send(f"{joke_data['setup']}\n{joke_data['delivery']}")
            else:
                await ctx.send("Couldn't fetch a dark joke at the moment.")
        else:
            await ctx.send("Couldn't fetch a dark joke at the moment.")
    else:
        await ctx.send("Couldn't fetch a dark joke at the moment.")

# Run the bot
bot.run(BOT_TOKEN)
