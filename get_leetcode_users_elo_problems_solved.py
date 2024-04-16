import requests
import json
import requests
import json
import boto3

# AWS SDK setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Specify your region
table = dynamodb.Table('LeetcodeUsers')  # Replace 'YourTableName' with the actual name of your DynamoDB table

# Define the headers and cookies as given in your template
cookies = {
    "__cf_bm": "KfeyV.YLeo6t2K1juP8yTRXTpS61xi17rRtY_Vb4Z.s-1713038425-1.0.1.1-aJPXvRWJ08BDACfr94Z9RIsO5IdL5X22fVIfyOMc2xVQ0.rDzCDu556AjP56lJMWS1HUQRA_eOh0wnqB_kB4SA",
    "__stripe_mid": "a80e1a68-7d69-4861-93d6-94410de982beda7d04",
    "_dd_s": "rum=0&expire=1713039327690",
    "_ga": "GA1.2.952786075.1680444489",
    "_ga_CDRWKZTDEX": "GS1.1.1680984327.14.1.1680986369.0.0.0",
    "cf_clearance": "6L1fZ1j9QOrv2ZpnoLWQddvQ0TbQ.ci76SV.FASBgxo-1711320670-1.0.1.1-fGKz6gtcvt4gVWnvfanmXnb5AMiVp3d4BzEKCjviDNiUnCI1Ipr1Y9Ui1t6JQna6Xz.bvgnL_OyvPtQqwKCPsA",
    "csrftoken": "8Ug0OkL0xOg1LmIiUtBBXReEfRMgY2FOUe3dgJfagv52YPEfHbG9n4b2BUpb7t7a",
    "gr_user_id": "ce2b8790-e558-4331-a8fe-6ef19c1a6c48",
    "INGRESSCOOKIE": "b2fb09370ce59ce7fecc5d38984fa337|8e0876c7c1464cc0ac96bc2edceabd27",
    "LEETCODE_SESSION": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTE2MzE0NCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImU2OWFhMWM2MWE5YzhiNDZhNmI0OThhNzFiY2M2NTg3NWNiYjI5M2FjZjc1YmZkZGE3NWU4NThjNTI5ZTRiODEiLCJpZCI6MTE2MzE0NCwiZW1haWwiOiJkYXJrbW9vbmtuaWdodF8yQGhvdG1haWwuY29tIiwidXNlcm5hbWUiOiJUaGVSZWFsUmF5bW9uZEpvbmVzIiwidXNlcl9zbHVnIjoiVGhlUmVhbFJheW1vbmRKb25lcyIsImF2YXRhciI6Imh0dHBzOi8vYXNzZXRzLmxlZXRjb2RlLmNvbS91c2Vycy9hdmF0YXJzL2F2YXRhcl8xNzAwMTYxOTY2LnBuZyIsInJlZnJlc2hlZF9hdCI6MTcxMzAxODE4MCwiaXAiOiIyODAwOjQ4NDo5MDdiOjVhMDA6MTlmYzoyYWU6OTA1MTo0NmQ2IiwiaWRlbnRpdHkiOiI3NTI3"
}

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
        response = table.put_item(
            Item={
                'username': user,
                'elo': elo,
                'problems_solved': problems_solved_count
            }
        )
        print(f"Data written to DynamoDB for user {user}: {response}")

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
