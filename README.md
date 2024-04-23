# discord_bot_practice

I wanted to create a way to see the Leetcode stats of your friends and rank them based on the amount of problems they solve every week. 

This competitiveness can help what feels like an isolated practice have a stronger community feeling. And thus, help everyone practice and improve along the way.

# Design and Flow

This is a discord bot hosted on AWS EC2.

It queries the Leetcode API to collect leetcode problem solved counts by users. Then, it forms a leaderboard with them and stores the data into DynamoDB.

Whenver a user in discord types "!leaderboard" it sends the leaderboard over into the Discord channel. 
