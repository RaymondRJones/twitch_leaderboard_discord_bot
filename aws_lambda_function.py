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
    message_lines = ["Player Rankings:"]
    for rank, item in enumerate(sorted_items, start=1):
        line = f"{rank}. {item['username']} - Elo: {item['elo']}"
        message_lines.append(line)
    full_message = "\n".join(message_lines)

    # Discord webhook setup
    webhook_url = os.getenv(WEBHOOK_URL)  # Environment variable for the webhook URL
    webhook = DiscordWebhook(url=webhook_url, content=full_message)

    # Send message to Discord
    response = webhook.execute()

    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to Discord successfully!')
    }

