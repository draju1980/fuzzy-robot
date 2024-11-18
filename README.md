# Notification Script

This Python script reads the latest message from an RSS feed and sends notifications to Discord, Slack, and Telegram based on specific conditions. Scheduled tasks or activity alerts are sent only at midnight, while all other messages are delivered immediately.

## Prerequisites

- Python 3.13 or higher
- `pip` (Python package installer)
- `python-dotenv` package

## Installation

1. Clone the repository:
```sh
git clone https://github.com/draju1980/fuzzy-robot.git
cd fuzzy-robot
```

2. Install the required Python packages:
```sh
pip3 install -r requirements.txt
```

3. Create a .env file in the root directory of the project and add your webhook URLs and tokens:
```sh
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/yyy
TELEGRAM_BOT_TOKEN=xxxx
TELEGRAM_CHAT_ID=yyyyy
```

Usage
Run the script:
```sh
python3 notification.py 
```

The script will read the latest message from the RSS feed and send notifications to Discord, Slack, and Telegram based on the following conditions:

*   If the message is a scheduled event and the current hour is midnight, it will send the message.
*   If the message is not a scheduled event, it will send the message immediately.

## GitHub Actions
This repository includes a GitHub Actions workflow that runs the script every hour. The workflow is defined in .github/workflows/main.yml.

To use GitHub Actions, make sure to add the following secrets from GitHub repository:

*   DISCORD_WEBHOOK
*   SLACK_WEBHOOK
*   TELEGRAM_BOT_TOKEN
*   TELEGRAM_CHAT_ID
