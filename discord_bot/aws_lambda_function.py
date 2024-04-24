import json
import os
import boto3
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
load_dotenv()
WEBHOOK_URL = os.getenv('PROD_WEBHOOK')
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('LeetcodeUsers')  # Updated table name to reflect its purpose

    response = table.scan() # grab DB table elements
    items = response['Items']

    sorted_items = sorted(items, key=lambda x: x['elo'], reverse=True)

    message_lines = ["Here are a list of the players ranked by elo"]
    message_lines.append("-------------")
    for rank, item in enumerate(sorted_items, start=1):
        if rank == 0:
            line = f" The Best Player Today -> {rank}. {item['username']} ({item['elo']}) - Problems Solved: {item['problem_solved']}"
        else:
            line = f"#{rank}. {item['username']} ({item['elo']}) - Problems Solved: {item['problems_solved']}"
        message_lines.append(line)
    full_message = "\n".join(message_lines)

    webhook_url = WEBHOOK_URL 
    webhook = DiscordWebhook(url=webhook_url, content=full_message)

    # Send message to Discord
    response = webhook.execute()

    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to Discord successfully!')
    }
