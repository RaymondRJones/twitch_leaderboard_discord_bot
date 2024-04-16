import json
import os
import boto3
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
load_dotenv()
WEBHOOK_URL = os.getenv('PROD_WEBHOOK')
def lambda_handler(event, context):
    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('LeetcodeUsers')  # Updated table name to reflect its purpose

    # Scan the entire table to get all items
    response = table.scan()
    items = response['Items']

    # Sort items by 'elo' in descending order
    sorted_items = sorted(items, key=lambda x: x['elo'], reverse=True)

    # Construct the message to send to Discord
    message_lines = ["Here are a list of the players ranked by elo"]
    message_lines.append("-------------")
    for rank, item in enumerate(sorted_items, start=1):
        if rank == 0:
            line = f" The Best Player Today -> {rank}. {item['username']} ({item['elo']}) - Problems Solved: {item['problem_solved']}"
        else:
            line = f"#{rank}. {item['username']} ({item['elo']}) - Problems Solved: {item['problems_solved']}"
        message_lines.append(line)
    full_message = "\n".join(message_lines)

    # Hardcoded Discord webhook setup
    # webhook_url = 'https://discord.com/api/webhooks/1229821635180105788/SrnGPWVbDa2kUha2qW0TDK71Wwgxnuibx09kGrIKTQncNx1L2IG5is8IwirXfZ4BEopr'
    webhook_url = 'https://discord.com/api/webhooks/1229877765503979702/IcFNxzw6cdjDUe7FjondrWOFR0m73xHYFXOcCFRmv5W0rhnMTP9zetz_3DOOoABPxIsd'
    webhook = DiscordWebhook(url=webhook_url, content=full_message)

    # Send message to Discord
    response = webhook.execute()

    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to Discord successfully!')
    }
