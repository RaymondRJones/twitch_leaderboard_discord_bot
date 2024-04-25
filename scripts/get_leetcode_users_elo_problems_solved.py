import requests
import json
import requests
import json
import boto3
from cookies import cookies
# AWS SDK setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Specify your region
table = dynamodb.Table('LeetcodeUsers')  # Replace 'YourTableName' with the actual name of your DynamoDB table

# Define the headers and cookies as given in your template
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0'
}
def get_problems_solved(username):
    url = "https://leetcode.com/graphql"
    payload = {
        "operationName": "userProblemsSolved",
        "query": """
        query userProblemsSolved($username: String!) {
            allQuestionsCount {
                difficulty
                count
            }
            matchedUser(username: $username) {
                problemsSolvedBeatsStats {
                    difficulty
                    percentage
                }
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
        }
        """,
        "variables": {"username": username}
    }
    response = requests.post(url, headers=headers, cookies=cookies, json=payload)
    if response.status_code == 200:
        data = response.json()
        total_problems_solved = data['data']['matchedUser']['submitStatsGlobal']['acSubmissionNum'][0]['count']
        return total_problems_solved
    else:
        print(f'Failed to retrieve problem stats for {username}: {response.status_code}')
        return None

def get_elo_of_leetcoder(username):
    url = "https://leetcode.com/graphql"
    payload = {
        "operationName": "userContestRankingInfo",
        "query": """
        query userContestRankingInfo($username: String!) {
            userContestRanking(username: $username) {
                rating
            }
        }
        """,
        "variables": {"username": username}
    }
    response = requests.post(url, headers=headers, cookies=cookies, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data['data']['userContestRanking']['rating']
    else:
        print('Failed to retrieve data for {}: {}'.format(username, response.status_code))
        return None

def read_usernames_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def save_data_to_dynamodb(user_data):
    for user, elo, problems_solved_count in user_data:
        response = table.get_item(
            Key={'username': user}
        )
        item = response.get('Item', {})
        last_week_problems_solved = item.get('problems_solved', 0)  # default to 0 if not found

        problems_solved_since_last_week = problems_solved_count - last_week_problems_solved

        response = table.put_item(
            Item={
                'username': user,
                'elo': elo,
                'problems_solved': problems_solved_count,
                'problems_solved_last_week': last_week_problems_solved,  # Update last week's count to current
                'problems_solved_since_last_week': problems_solved_since_last_week  # Store the computed difference
            }
        )
        print(f"Data updated in DynamoDB for user {user}: {response}")


def main():
    usernames = read_usernames_from_file('usernames.txt')
    user_data = []
    for username in usernames:
        print("Getting elo of...", username)
        elo = int(get_elo_of_leetcoder(username))
        problems_solved_count = get_problems_solved(username)
        if elo is not None:
            user_data.append((username, elo, problems_solved_count))
            print("Success! Adding value of elo", elo, "to", username)
    save_data_to_dynamodb(user_data)

if __name__ == "__main__":
    main()
