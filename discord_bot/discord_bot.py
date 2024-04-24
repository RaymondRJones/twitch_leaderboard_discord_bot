import discord
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Retrieve the bot token and webhook URL from environment variables
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Enable message content intent

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!leaderboard"):
        print("Received leaderboard command")
        try:
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('LeetcodeUsers')
            response = table.scan()
            items = response['Items']

            sorted_items = sorted(items, key=lambda x: x.get('problems_solved_since_last_week', 0), reverse=True)

            message_lines = ["📊 **Leaderboard: Problems Solved Since Last Week**"]
            message_lines.append("---------------------------------------------------")
            for rank, item in enumerate(sorted_items, start=1):
                problems_solved_since_last_week = item.get('problems_solved_since_last_week', 0)
                total_problems_solved = item.get('problems_solved', 0)
                sign = "+" if problems_solved_since_last_week >= 0 else ""
                line = f"#{rank}. {item['username']} ({sign}{problems_solved_since_last_week} since last week) - Total: {total_problems_solved}"
                message_lines.append(line)

            full_message = "\n".join(message_lines)
            await message.channel.send(full_message)
        except Exception as e:
            print(f"An error occurred: {e}")  # Print out any errors
            await message.channel.send("Failed to retrieve the leaderboard due to an internal error.")


client.run(BOT_TOKEN)
 