import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import discord_bot

class TestDiscordBot(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('discord_bot.discord.Client', autospec=True)
        self.mock_client = self.patcher.start()
        self.addCleanup(self.patcher.stop)

        self.mock_client.user = MagicMock()
        self.mock_client.user.id = 12345

    @patch('discord_bot.boto3.resource')
    async def test_leaderboard_command(self, mock_boto3):
        mock_message = AsyncMock()
        mock_message.content = "!leaderboard"
        mock_message.channel = AsyncMock()
        mock_message.author.id = 67890

        mock_table = mock_boto3.return_value.Table.return_value
        mock_table.scan.return_value = {
            'Items': [
                {'username': 'user1', 'problems_solved_since_last_week': 5, 'problems_solved': 50},
                {'username': 'user2', 'problems_solved_since_last_week': 3, 'problems_solved': 30}
            ]
        }

        await discord_bot.on_message(mock_message)

        assert mock_message.channel.send.call_count == 1
        expected_message = ("\n".join([
            "📊 **Leaderboard: Problems Solved Since Last Week**",
            "---------------------------------------------------",
            "#1. user1 (+5 since last week) - Total: 50",
            "#2. user2 (+3 since last week) - Total: 30"
        ]))
        mock_message.channel.send.assert_called_with(expected_message)

    def test_environment_variable_loading(self):
        self.assertIsNotNone(discord_bot.BOT_TOKEN)

if __name__ == '__main__':
    unittest.main()

