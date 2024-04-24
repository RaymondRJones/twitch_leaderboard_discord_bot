# Leetcode Leaderboard with Friends (Discord Bot)

I wanted to create a way to see the Leetcode stats of your friends and rank them based on the amount of problems they solve every week. 

This competitiveness can help what feels like an isolated practice have a stronger community feeling. And thus, help everyone practice and improve along the way.

# To Run

1. clone this repo
2. cd into `discord_bot`

Go to Discord Developer and create a bot with a bot token
Add bot token into your `.env`

run `python discord_bot.py`

You may need configure your AWS for `boto3` if you haven't already
You can run `aws configure` and type in your AWS account access code. This will allow you to store data into DynamoDB

# Design and Flow

This is a discord bot hosted on AWS EC2.

It queries the Leetcode API to collect leetcode problem solved counts by users. Then, it forms a leaderboard with them and stores the data into DynamoDB.

Whenver a user in discord types "!leaderboard" it sends the leaderboard over into the Discord channel. 
